package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.Patient;
import com.healthmas.util.*;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class TriageAgent extends BDIAgent {
    @Override
    protected void setup() {
        super.setup();
        addBehaviour(new TriageRequestReceiverBehaviour());
        System.out.println("[" + getLocalName() + "] Triage agent ready.");
    }

    @Override protected void initBeliefs() { beliefBase.set("triageCount", 0); }

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "EvaluateAndForwardPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof AssessUrgencyGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                AssessUrgencyGoal g = (AssessUrgencyGoal) goal;
                Patient patient = g.getPatient();
                int score = UrgencyEvaluator.evaluate(patient);
                beliefs.set("triageCount", (int) beliefs.get("triageCount") + 1);

                System.out.println("[" + getLocalName() + "] Triaged " + patient.getName() + " -> level=" + patient.getUrgencyLevel());
                ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                reply.addReceiver(new AID(MsgOntology.SCHEDULER_AGENT, AID.ISLOCALNAME));
                reply.setOntology(MsgOntology.TRIAGE_RESULT);
                reply.setContent(patient.toAclString() + "||" + g.getReplyToAID());
                send(reply);
            }
        });
    }

    private class TriageRequestReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST), MessageTemplate.MatchOntology(MsgOntology.TRIAGE_REQUEST));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                addGoal(new AssessUrgencyGoal(Patient.fromAclString(msg.getContent()), msg.getSender().getLocalName()));
            } else block();
        }
    }
}
