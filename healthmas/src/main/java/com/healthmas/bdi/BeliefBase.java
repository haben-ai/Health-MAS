package com.healthmas.bdi;

import java.util.LinkedHashMap;
import java.util.Map;

public class BeliefBase {
    private final Map<String, Object> beliefs = new LinkedHashMap<>();

    public void set(String name, Object value) { beliefs.put(name, value); }
    public Object get(String name) { return beliefs.get(name); }
    public Object getOrDefault(String name, Object def) { return beliefs.getOrDefault(name, def); }
    public boolean has(String name) { return beliefs.containsKey(name); }
    public void remove(String name) { beliefs.remove(name); }

    public void print(String agentName) {
        System.out.println("[" + agentName + "] BeliefBase:");
        beliefs.forEach((k, v) -> System.out.println("  " + k + " = " + v));
    }
}
