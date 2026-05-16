package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.*;
import com.healthmas.util.*;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class NegotiatorAgent extends BDIAgent {
    @Override
    protected void setup() {
        super.setup();
        addBehaviour(new NegotiateRequestReceiverBehaviour());
        System.out.println("[" + getLocalName() + "] Negotiator agent ready.");
    }

    @Override protected void initBeliefs() {}

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "RankAndReschedulePlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof ResolveConflictGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                ResolveConflictGoal g = (ResolveConflictGoal) goal;
                Patient urgent = g.getUrgentPatient();

                List<DoctorSlot> booked = ScheduleDB.getInstance().findReschedulableSlotsForSpecialty(urgent.getRequiredSpecialty());
                Optional<DoctorSlot> targetSlotOpt = booked.stream().filter(s -> s.getBookedPatient() != null).min(Comparator.comparingInt(s -> s.getBookedPatient().getUrgencyScore()));

                if (targetSlotOpt.isEmpty()) return;
                DoctorSlot targetSlot = targetSlotOpt.get();
                Patient displaced = targetSlot.getBookedPatient();

                if (!urgent.getUrgencyLevel().isMoreUrgentThan(displaced.getUrgencyLevel())) return;

                System.out.println("[" + getLocalName() + "] Preempting booking! Displacing: " + displaced.getName() + " for Urgent Intake: " + urgent.getName());
                ScheduleDB.getInstance().freeSlot(targetSlot.getSlotId());

                ACLMessage notice = new ACLMessage(ACLMessage.INFORM);
                notice.addReceiver(new AID(displaced.getPatientId(), AID.ISLOCALNAME));
                notice.setOntology(MsgOntology.RESCHEDULE_NOTIFY);
                notice.setContent("Your booking has been bumped down due to an emergency. Alternate allocations will follow.");
                send(notice);

                ACLMessage result = new ACLMessage(ACLMessage.INFORM);
                result.addReceiver(new AID(g.getSchedulerAID(), AID.ISLOCALNAME));
                result.setOntology(MsgOntology.NEGOTIATE_RESULT);
                result.setContent(urgent.toAclString() + "||" + targetSlot.getSlotId());
                send(result);
            }
        });
    }

    private class NegotiateRequestReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST), MessageTemplate.MatchOntology(MsgOntology.NEGOTIATE_REQUEST));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String[] parts = msg.getContent().split("\\|\\|", 2);
                addGoal(new ResolveConflictGoal(Patient.fromAclString(parts[0]), parts[1]));
            } else block();
        }
    }
}
