/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package wfrpovtestcases;

import javax.swing.JTextArea;

/**
 *
 * @author DGarijo
 */
public class ThreadForQueries extends Thread{
    CheckTestCases ck;
    JTextArea text;
    int selection;
    
    public ThreadForQueries(CheckTestCases c, JTextArea textArea, int number){
        ck = c;
        text = textArea;
        selection = number;
    }
    
    @Override
    public void run(){
        String tcResult = "";
        switch (selection){
            case 1: tcResult = ck.checkTestCase1();break;
            case 2: tcResult = ck.checkTestCase2();break;
            case 3: tcResult = ck.checkTestCase3();break;
            case 4: tcResult = ck.checkTestCase4();break;
            case 5: tcResult = ck.checkTestCase5();break;
            case 6: tcResult = ck.checkTestCase6();break;
            case 7: tcResult = ck.checkTestCase7();break;
            case 8: tcResult = ck.checkTestCase8();break;
            case 9: tcResult = ck.checkTestCase9();break;
            case 10: tcResult = ck.checkTestCase10();break;
            case 11: tcResult = ck.checkTestCase11();break;
            case 12: tcResult = ck.checkTestCase12();break;
            case 13: tcResult = ck.checkTestCase13();break;
            case 14: tcResult = ck.checkTestCase14();break;
            case 15: tcResult = ck.checkTestCase15();break;
            case 16: tcResult = ck.checkTestCase16();break;
            case 17: tcResult = ck.checkTestCase17();break;
        }
        text.append("Test Case "+selection+": "+ tcResult + "\n");
    }
}
