package com.healthmas.scenario;

import com.healthmas.agents.*;
import com.healthmas.model.*;
import com.healthmas.util.ScheduleDB;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentContainer;

public class Scenario2Launcher {
    public static void main(String[] args) throws Exception {
        System.out.println("=== Running HealthMAS Scenario 2 ===");
        ScheduleDB.getInstance().seedFullyBookedCardiologist();

        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        p.setParameter(Profile.MAIN_HOST, "localhost");
        p.setParameter(Profile.GUI, "true");
        AgentContainer container = rt.createMainContainer(p);

        container.createNewAgent("TriageAgent", TriageAgent.class.getName(), null).start();
        container.createNewAgent("SchedulerAgent", SchedulerAgent.class.getName(), null).start();
        container.createNewAgent("NegotiatorAgent", NegotiatorAgent.class.getName(), null).start();

        Thread.sleep(300);
        Patient alice = new Patient("P-LOW1", "Alice Brown", "mild fatigue", "Cardiology");
        alice.setUrgencyScore(2); alice.setUrgencyLevel(UrgencyLevel.LOW);
        container.createNewAgent("P-LOW1", PatientAgent.class.getName(), new Object[]{alice}).start();

        Patient bob = new Patient("P-LOW2", "Bob Wilson", "routine check", "Cardiology");
        bob.setUrgencyScore(2); bob.setUrgencyLevel(UrgencyLevel.LOW);
        container.createNewAgent("P-LOW2", PatientAgent.class.getName(), new Object[]{bob}).start();

        Thread.sleep(300);
        Patient fatima = new Patient("P002", "Fatima Al-Hassan", "chest pain and difficulty breathing", "Cardiology");
        container.createNewAgent("PatientAgent-P002", PatientAgent.class.getName(), new Object[]{fatima}).start();
    }
}
