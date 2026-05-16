package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.*;
import com.healthmas.util.MsgOntology;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class PatientAgent extends BDIAgent {
    private Patient patient;

    @Override
    protected void setup() {
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            patient = (Patient) args[0];
        } else {
            patient = new Patient("P000", "Default Patient", "headache", "GP");
        }
        super.setup();

        beliefBase.set("patient", patient);
        beliefBase.set("status", "waiting");

        addBehaviour(new ConfirmationReceiverBehaviour());
        addBehaviour(new RescheduleNotifyReceiverBehaviour());

        if (patient.getUrgencyScore() == 0) {
            addGoal(new GetTriagedGoal(patient));
        }
        System.out.println("[" + getLocalName() + "] Started for patient: " + patient);
    }

    @Override protected void initBeliefs() {}

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "SendToTriagePlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof GetTriagedGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                Patient p = ((GetTriagedGoal) goal).getPatient();
                ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
                msg.addReceiver(new jade.core.AID(MsgOntology.TRIAGE_AGENT, jade.core.AID.ISLOCALNAME));
                msg.setOntology(MsgOntology.TRIAGE_REQUEST);
                msg.setContent(p.toAclString());
                send(msg);
            }
        });

        planLibrary.add(new Plan() {
            @Override public String getName() { return "HandleConfirmationPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof ConfirmAppointmentGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                Appointment appt = ((ConfirmAppointmentGoal) goal).getAppointment();
                beliefs.set("appointment", appt);
                beliefs.set("status", "confirmed");
                System.out.println("[" + getLocalName() + "] * APPOINTMENT CONFIRMED: " + appt);
            }
        });
    }

    private class ConfirmationReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.CONFIRM), MessageTemplate.MatchOntology(MsgOntology.APPOINTMENT_CONFIRM));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String content = msg.getContent();
                String[] parts = content.split("\\|", -1);
                DoctorSlot slot = new DoctorSlot(parts[7], parts[8], "?", parts[9]);
                Appointment appt = Appointment.fromAclString(content, slot);
                addGoal(new ConfirmAppointmentGoal(appt));
            } else block();
        }
    }

    private class RescheduleNotifyReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.MatchOntology(MsgOntology.RESCHEDULE_NOTIFY);
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                System.out.println("[" + myAgent.getLocalName() + "] ! RESCHEDULE NOTICE: " + msg.getContent());
                beliefBase.set("status", "rescheduled");
            } else block();
        }
    }
}
