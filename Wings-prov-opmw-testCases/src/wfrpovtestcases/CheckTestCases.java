/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package wfrpovtestcases;

import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

/**
 * Class that does individual checks for the test cases.
 * The queries for the test cases are defined in the QueriesTestCases Class.
 * @author DGarijo
 */
public class CheckTestCases {
    
    /**
     * Find out the workflow executed from a run id
     */
    public String checkTestCase1(){        
        String queryTest1 = QueriesTestCases.getQueryTestCase1(Constants.runId);
        String definition = "Find out the workflow template from a run id\n";
        int count = testQueryToRepository("workflow", queryTest1);        
        if (count >1){
            return definition+"....Fail: the run from id "+Constants.runId+" belongs to more than one workflow template";
        }else{
            return definition+"....OK";
        }
    }
    
    /**
     * Find out the runs of a particular workflow.
     */
    public String checkTestCase2(){
        //There must be at least one execution per workflow
        String definition = "Find out the runs of a particular workflow.\n";
        String queryTest2 = QueriesTestCases.getQueryTestCase2(Constants.templateID);
        int count = testQueryToRepository("run", queryTest2);        
        if (count <1){
            return definition+"....Fail: no runs have been found for workflows with id "+Constants.templateID;
        }else{
            return definition+"....OK";
        }
    }
     /**
     * Find out the number of outputs of a particular run.
     */
    public String checkTestCase3(){
        //The number of outputs must be at least 1 (unless the workflow execution has failed)
        String definition = "Find out the outputs of a particular run.\n";
        String queryTest3a = QueriesTestCases.getQueryTestCase3a(Constants.runId); 
        System.out.println(queryTest3a);
        String returnResult = "";
        int count = this.testQueryToRepository("entity", queryTest3a);
        if (count <1){
            returnResult = definition+ "....Fail: no outputs have been found for the run with id "+Constants.runId+" (PROV) \n";
        }else{
            returnResult = definition+ "....OK (PROV)\n";
        }
        String queryTest3b = QueriesTestCases.getQueryTestCase3b(Constants.runId);        
        System.out.println(queryTest3b);
        count = this.testQueryToRepository("entity", queryTest3b);           
        if (count <1){
            return returnResult +=  "....Fail: no outputs have been found for the run with id "+Constants.runId+" (OPMW) ";
        }else{
            return returnResult +=  "....OK (OPMW)";
        }
        
    }
    
    //check the number of inputs of a given run
    public String checkTestCase4(){
        String definition = "Find out the intputs of a particular run.\n";
        //a run must have at least one input
        String queryTest4a = QueriesTestCases.getQueryTestCase4a(Constants.runId);
        System.out.println(queryTest4a);
        String returnResult = "";
        int count = this.testQueryToRepository("entity", queryTest4a);
        if (count <1){
            returnResult = definition+ "....Fail: no outputs have been found for the run with id "+Constants.runId+" (PROV) \n";
        }else{
            returnResult = definition+ "....OK (PROV)\n";
        }
        
        String queryTest4b = QueriesTestCases.getQueryTestCase4b(Constants.runId);  
        System.out.println(queryTest4b);
        count = testQueryToRepository("entity", queryTest4b);        
        if (count <1){
            return returnResult +=  "....Fail: no outputs have been found for the run with id "+Constants.runId+" (OPMW) ";
        }else{
            return returnResult +=  "....OK (OPMW)";
        }
    }
    
    //Find out the processes executed in a particular run.
    public String checkTestCase5(){
        String definition = "Find out the processes executed in a particular run.\n";
        //If no processes were executed, then it fails
        String queryTest5a = QueriesTestCases.getQueryTestCase5a(Constants.runId);  
        System.out.println(queryTest5a);
        String returnResult = "";
        int count = testQueryToRepository("process", queryTest5a);
        if (count <1){
            returnResult = definition+ "....Fail: no processes have been found for the run with id "+Constants.runId+" (PROV) \n";
        }else{
            returnResult = definition+ "....OK (PROV)\n";
        }        
        String queryTest5b = QueriesTestCases.getQueryTestCase5b(Constants.runId);
        System.out.println(queryTest5b);
        count = testQueryToRepository("process", queryTest5b);       
        if (count <1){
            return returnResult +=  "....Fail: no processes have been found for the run with id "+Constants.runId+" (OPMW) ";
        }else{
            return returnResult +=  "....OK (OPMW)";
        }
    }
    
    //Find out the services executed for all the processes taken place in a particular run.
    public String checkTestCase6(){
        String definition = "Find out the services executed for all the processes taken place in a particular run.\n";
        //fails if no processes have been executed.
        //If needed, this query could provide the location of the components executed
        String queryTest6 = QueriesTestCases.getQueryTestCase6(Constants.runId);  
        System.out.println(queryTest6);
        int count = testQueryToRepository("process", queryTest6);        
        if (count <1){
            return definition+"....Fail: No processes have been executed for run: "+Constants.runId;
        }else{
            return definition+"....OK";
        }
    }
    
    //Find out which inputs belonged to each process, given a run
    public String checkTestCase7(){
        String definition = "Find out which inputs belonged to each process, given a run.\n";
        //If no processes were executed, then it fails
        String queryTest7a = QueriesTestCases.getQueryTestCase7a(Constants.runId); 
        System.out.println(queryTest7a);
        String returnResult = "";
        int count = testQueryToRepository("process", queryTest7a);
        if (count <1){
            returnResult = definition+ "....Fail: no processes have been found for the run with id "+Constants.runId+" (PROV) ";
        }else{
            returnResult = definition+ "....OK (PROV)";
        }        
        String queryTest7b = QueriesTestCases.getQueryTestCase7b(Constants.runId);
        System.out.println(queryTest7b);
        count = testQueryToRepository("process", queryTest7b);       
        if (count <1){
            return returnResult +=  "....Fail: no processes have been found for the run with id "+Constants.runId+" (OPMW)";
        }else{
            return returnResult +=  "....OK (OPMW)";
        }
    }
    
    //Find out what outputs were produced by a particular process
    public String checkTestCase8(){
        String definition = "Find out what outputs were produced by a particular process\n";
        //If no entities are generated then it fails
        String queryTest8a = QueriesTestCases.getQueryTestCase8a(Constants.workflowExecutionProcessID);        
        System.out.println(queryTest8a);
        String returnResult = "";
        int count = testQueryToRepository("entity", queryTest8a);
        if (count <1){
            returnResult = definition+ "....Fail: the process with ID "+Constants.workflowExecutionProcessID+" does not generate any entities (PROV) \n";
        }else{
            returnResult = definition+ "....OK (PROV)\n";
        }        
        String queryTest8b = QueriesTestCases.getQueryTestCase8b(Constants.workflowExecutionProcessID);
        System.out.println(queryTest8b);
        count = testQueryToRepository("entity", queryTest8b);       
        if (count <1){
            return returnResult +=  "....Fail: the process with ID "+Constants.workflowExecutionProcessID+" does not generate any entities (OPMW)";
        }else{
            return returnResult +=  "....OK (OPMW)";
        }
    }
    
    //Find out when the workflow run was started
    public String checkTestCase9(){
        String definition = "Find out when the workflow run was started\n";
        //fails if no time is recorded        
        String queryTest9 = QueriesTestCases.getQueryTestCase9(Constants.runId); 
        System.out.println(queryTest9);
        int count = testQueryToRepository("time", queryTest9);        
        if (count <1){
            return definition+"....Fail: No starting time for run: "+Constants.runId;
        }else{
            return definition+"....OK";
        }
    }
    
    //Find out when the workflow run finished
    public String checkTestCase10(){
        String definition = "Find out when the workflow run finished\n";
        //fails if no time is recorded        
        String queryTest10 = QueriesTestCases.getQueryTestCase10(Constants.runId);    
        System.out.println(queryTest10);
        int count = testQueryToRepository("time", queryTest10);        
        if (count <1){
            return definition +"....Fail: No starting time for run: "+Constants.runId;
        }else{
            return definition +"....OK";
        }
    }
    
    
    //Find out who executed the workflow
    public String checkTestCase11(){
        String definition = "Find out who executed the workflow\n";
        //fails if no author is recorded     
        String queryTest11 = QueriesTestCases.getQueryTestCase11a(Constants.runId);        
        System.out.println(queryTest11);
        int count = testQueryToRepository("author", queryTest11);        
        if (count <1){
            return definition+"....Fail: No authors for run: "+Constants.runId;
        }else{
            return definition+"....OK";
        }
    }
    
    //Find out the executions that failed and the workflow they belong to.
    public String checkTestCase12(){
        String definition = "Find out the executions that failed and the workflow they belong to\n";
        //fails if no execution has failed     
        String queryTest12 = QueriesTestCases.getQueryTestCase12();
        System.out.println(queryTest12);
        int count = testQueryToRepository("account", queryTest12);        
        if (count <1){
            return definition+"....Fail: No executions have failed";
        }else{
            return definition+"....OK";
        }
    }
    
    //Tell me for each workflow the successful executions I can find.
    public String checkTestCase13(){
        String definition = "Tell me for each workflow the successful executions I can find.\n";
        //fails if no workflows are found     
        String queryTest13 = QueriesTestCases.getQueryTestCase13();   
        System.out.println(queryTest13);
        int count = testQueryToRepository("wf", queryTest13);        
        if (count <1){
            return definition+"....Fail: No workflows have been found";
        }else{
            return definition+"....OK";
        }
    }
    
    //Given a specific component of the component catalog/service, in which templates is it used? 
    public String checkTestCase14(){
        String definition = "Given a specific component of the component catalog/service, in which templates is it used?.\n";
        //fails if no usages of the component are found     
        String queryTest14 = QueriesTestCases.getQueryTestCase14(Constants.componentID); 
        System.out.println(queryTest14);
        int count = testQueryToRepository("templ", queryTest14);        
        if (count <1){
            return definition+"....Fail: No usages of component "+Constants.componentID+" have been found";
        }else{
            return definition+"....OK";
        }
    }
    
    //What are the most used components across the workflows? How many times are they used?
    public String checkTestCase15(){
        String definition = "What are the most used components across the workflows? How many times are they used.\n";
        //fails if no common components are found
        String queryTest15 = QueriesTestCases.getQueryTestCase15();
        System.out.println(queryTest15);
        int count = testQueryToRepository("process", queryTest15);        
        if (count <1){
            return definition+"....Fail: No common components have been found";
        }else{
            return definition+"....OK";
        }
    }
    
    //Give me the title/name of a workflow
    public String checkTestCase16(){
        String definition = "Title/name of the workflow (label).\n";
        //fails if no usages of the component are found     
        String queryTest16 = QueriesTestCases.getQueryTestCase16(Constants.templateID); 
        System.out.println(queryTest16);
        int count = testQueryToRepository("title", queryTest16);        
        if (count <1){
            return definition+"....Fail: No title found for "+Constants.templateID+" have been found";
        }else{
            return definition+"....OK";
        }
    }
    
    //Who designed the workflow?
    public String checkTestCase17(){
        String definition = "Designer of the workflow.\n";
        //fails if no usages of the component are found     
        String queryTest17 = QueriesTestCases.getQueryTestCase17(Constants.templateID); 
        System.out.println(queryTest17);
        int count = testQueryToRepository("contributor", queryTest17);        
        if (count <1){
            return definition+"....Fail: No contributor found for "+Constants.templateID+" have been found";
        }else{
            return definition+"....OK";
        }
    }
    
    private int testQueryToRepository(String varToRetrieve, String query){
        ResultSet rs = performQueryToEndpoint(query);
        int count = 0;
        while (rs.hasNext()){
            QuerySolution qs = rs.next();
            String run ="";
            try{
                run = qs.getResource("?"+varToRetrieve).getURI();
                count++;
            }catch (Exception e){
                try{
                    run = qs.getLiteral("?"+varToRetrieve).getString();
                    count++;
                }catch(Exception e1){
                
                }
            }
            System.out.println(run);            
        }
        return count;
    }
    
    private ResultSet performQueryToEndpoint(String query){
        QueryExecution qe = QueryExecutionFactory.sparqlService(Constants.endpointURI, query);
        return qe.execSelect();
    }
    
}
