package com.example.ruleengine;

import org.kie.api.KieServices;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;

public class RuleEngineService {
    private KieSession kieSession;

    public void init() {
        try {
            KieServices ks = KieServices.Factory.get();
            KieContainer kc = ks.getKieClasspathContainer();
            
            // 验证KieContainer是否成功创建
            if (kc == null) {
                throw new RuntimeException("KieContainer creation failed");
            }
            
            kieSession = kc.newKieSession("ProblemLocatorKS");
            System.out.println("KieSession created: " + kieSession);
        } catch (Exception e) {
            System.err.println("规则引擎初始化失败:");
            e.printStackTrace();
            throw new RuntimeException("初始化错误", e);
        }
    }

    public String matchRules(ProblemContext context) {
        kieSession.insert(context);
        kieSession.fireAllRules();
        return context.getConclusion();
    }

    public static void main(String[] args) {
        System.setProperty("drools.dialect.java.compiler", "JANINO");
        System.setProperty("drools.dialect.java.compiler.lnglevel", "23");
        
        RuleEngineService engine = new RuleEngineService();

        try {
            engine.init();
        
            // 测试用例
            ProblemContext ctx = new ProblemContext();
            ctx.setLog("ERROR: interface eth0 DOWN");
            ctx.setCommand("show interface eth0 status=DOWN");
            
            engine.matchRules(ctx);
            System.out.println("结论：" + ctx.getConclusion());
        } catch (Exception e) {
            System.err.println("系统初始化失败:");
            e.printStackTrace();
        }
    }
}