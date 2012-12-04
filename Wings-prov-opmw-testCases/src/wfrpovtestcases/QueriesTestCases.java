/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package wfrpovtestcases;

/**
 *
 * @author DGarijo
 */
public class QueriesTestCases {
    public static String getQueryTestCase1(String runId){
        String query =  "select distinct ?workflow where {"+
                        "<"+runId+"> <http://www.opmw.org/ontology/correspondsToTemplate> ?workflow."+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase2(String templateID){
        String query = "select distinct ?run where {"+
                        "?run <http://www.opmw.org/ontology/correspondsToTemplate> <"+templateID+">"+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase3a(String runID){
        String query = "select distinct ?entity "+
                        "from <"+runID+"> "+
                        "where {"+
                        "?entity a <http://www.w3.org/ns/prov#Entity>."+
                        "?entity <http://www.w3.org/ns/prov#wasGeneratedBy> ?process."+
                        "FILTER NOT EXISTS"+
                        "{"+
                        "?process2 <http://www.w3.org/ns/prov#used> ?entity."+
                        "}"+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase3b(String runID){
        String query = "select distinct ?entity "+
                       "where {"+
                       "?entity <http://openprovenance.org/model/opmo#account> <"+runID+">."+
                       "?entity a <http://www.opmw.org/ontology/WorkflowExecutionArtifact>."+
                       "?entity <http://purl.org/net/opmv/ns#wasGeneratedBy> ?process."+
                       "FILTER NOT EXISTS"+
                       "{?process2 <http://purl.org/net/opmv/ns#used> ?entity.}"+                        
                        "}";
        return query;
    }
    
    public static String getQueryTestCase4a(String runID){
        String query = "select distinct ?entity "+
                       "from <"+runID+">"+
                       "where {"+
                       "?entity a <http://www.w3.org/ns/prov#Entity>."+
                       "?process <http://www.w3.org/ns/prov#used> ?entity."+
                       "FILTER NOT EXISTS"+
                       "{"+
                       "      ?entity <http://www.w3.org/ns/prov#wasGeneratedBy> ?process2."+
                       "}"+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase4b(String runID){
        String query = "select distinct ?entity "+
        "where {"+
        "?entity <http://openprovenance.org/model/opmo#account> <"+runID+">."+
        "?entity a <http://www.opmw.org/ontology/WorkflowExecutionArtifact>."+
        "?process <http://purl.org/net/opmv/ns#used> ?entity."+
        "FILTER NOT EXISTS"+
         "{"+
          "?entity <http://purl.org/net/opmv/ns#wasGeneratedBy> ?process2."+
         "}"+
        "}";
        return query;
    }
    
    public static String getQueryTestCase5a(String runID){
        String query = "select distinct ?process "+
        "from <"+runID+">"+
        "where {"+
        "?process a <http://www.w3.org/ns/prov#Activity>."+
        "}";
        return query;
    }

public static String getQueryTestCase5b(String runID){
    String query =  "select distinct ?process "+
        "where {"+
        "?process <http://openprovenance.org/model/opmo#account> <"+runID+">."+
        "?process a <http://www.opmw.org/ontology/WorkflowExecutionProcess>."+
        "}";
    return query;
    }
    
    public static String getQueryTestCase6(String runID){
        String query = "select distinct ?process ?l "+
        "where {"+
        "?process a <http://www.w3.org/ns/prov#Activity>."+
        "?process <http://openprovenance.org/model/opmo#account> <"+runID+"> ."+
        "?process <http://www.opmw.org/ontology/hasExecutableComponent> ?exec."+
        "?exec <http://www.w3.org/ns/prov#atLocation> ?l"+
        "}";
        return query;
    }
    
    public static String getQueryTestCase7a(String runID){
        String query = "select distinct ?process ?input "+
        "from <"+runID+">"+
        "where {"+
        "?process a <http://www.w3.org/ns/prov#Activity>."+
        "?process <http://www.w3.org/ns/prov#used> ?input  ."+
        "}";
        return query;
    }
    public static String getQueryTestCase7b(String runID){
        String query = "select distinct ?process ?input where {"+
            "?process <http://openprovenance.org/model/opmo#account> <"+runID+"> ."+
            "?process a <http://www.opmw.org/ontology/WorkflowExecutionProcess>."+
            "?process <http://purl.org/net/opmv/ns#used> ?input."+
            "}";
        return query;
    }
    
    public static String getQueryTestCase8a(String execProcessID){
        String query = "select distinct ?entity "+
                       "where {"+
                       "?entity a <http://www.w3.org/ns/prov#Entity>."+
                       "?entity <http://www.w3.org/ns/prov#wasGeneratedBy> <"+execProcessID+">"+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase8b(String execProcessID){ 
        String query = "select distinct ?entity "+
                        "where {"+
                        "?entity a <http://www.opmw.org/ontology/WorkflowExecutionArtifact>."+
                        "?entity <http://purl.org/net/opmv/ns#wasGeneratedBy> <"+execProcessID+">"+
                        "}";
        return query;
    }
    
    public static String getQueryTestCase9(String runID){
        String query = "select distinct ?time "+
                "where {"+
                "<"+runID+"> <http://www.opmw.org/ontology/overallStartTime> ?time"+
                "}";
        return query;
    }
    
    public static String getQueryTestCase10(String runID){
        String query = "select distinct ?time "+
                       "where {"+
                       "<"+runID+"> <http://www.opmw.org/ontology/overallEndTime> ?time}";
        return query;
    }
    
    public static String getQueryTestCase11a(String runID){
        String query = "select distinct ?author "+
                    "from <"+runID+">"+
                    "where {"+
                    "?process a <http://www.w3.org/ns/prov#Activity>."+
                    "?process <http://www.w3.org/ns/prov#wasAssociatedWith> ?author."+
                    "}";
        return query;
    }
    
    public static String getQueryTestCase12(){
        String query = "select distinct ?account ?wf "+
            "where {"+
            "?account a <http://www.opmw.org/ontology/WorkflowExecutionAccount>."+
            "?account <http://www.opmw.org/ontology/hasStatus> \"FAILURE\"."+
            "?account <http://www.opmw.org/ontology/correspondsToTemplate> ?wf"+
            "}";
        return query;
    }
    
    public static String getQueryTestCase13(){
        String query = "select distinct ?wf ?account "+
                "where {"+
                "?account a <http://www.opmw.org/ontology/WorkflowExecutionAccount>."+
                "?account <http://www.opmw.org/ontology/hasStatus> \"SUCCESS\"."+
                "?account <http://www.opmw.org/ontology/correspondsToTemplate> ?wf"+
                "}";
         return query;
    }
    
    public static String getQueryTestCase14(String componentID){
       String query = "select distinct ?templ ?process where {"+
            "?process a <"+componentID+">."+
            "?process <http://www.opmw.org/ontology/isStepOfTemplate> ?templ."+
            "}";
        return query;
    }
    
    public static String getQueryTestCase15(){
        String query = "select distinct ?componentType ?process where {"+
            "?process a <http://www.opmw.org/ontology/WorkflowTemplateProcess>."+
            "?process a ?componentType."+
            "FILTER regex(?componentType, \"/ac\")"+
            "}LIMIT 10";
        return query;
    }
    
    public static String getQueryTestCase16(String templateID){
        String query = "select distinct ?title where {"+
             "<"+templateID+"> a <http://www.opmw.org/ontology/WorkflowTemplate>."+
             "<"+templateID+"> <http://www.w3.org/2000/01/rdf-schema#label> ?title}";
        return query;
    }
    
    public static String getQueryTestCase17(String templateID){
        String query = "select distinct ?contributor where {"+            
            "<"+templateID+"> <http://purl.org/dc/terms/contributor> ?contributor."+
            //"<"+templateID+"> opmw:hasDocumentation ?doc"+
            "}";
        return query;
    }
}
