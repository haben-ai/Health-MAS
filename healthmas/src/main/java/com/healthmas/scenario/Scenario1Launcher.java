package com.healthmas.scenario;

import com.healthmas.agents.*;
import com.healthmas.model.Patient;
import com.healthmas.util.ScheduleDB;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentContainer;

public class Scenario1Launcher {
    public static void main(String[] args) throws Exception {
        System.out.println("=== Running HealthMAS Scenario 1 ===");
        ScheduleDB.getInstance().seedNormalSchedule();

        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        p.setParameter(Profile.MAIN_HOST, "localhost");
        p.setParameter(Profile.GUI, "true");
        AgentContainer container = rt.createMainContainer(p);

        container.createNewAgent("TriageAgent", TriageAgent.class.getName(), null).start();
        container.createNewAgent("SchedulerAgent", SchedulerAgent.class.getName(), null).start();
        container.createNewAgent("NegotiatorAgent", NegotiatorAgent.class.getName(), null).start();

        Thread.sleep(300);
        Patient john = new Patient("P001", "John Doe", "headache and dizziness", "GP");
        container.createNewAgent("PatientAgent-P001", PatientAgent.class.getName(), new Object[]{john}).start();
    }
}
