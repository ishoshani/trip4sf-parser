# -*- coding: utf-8 -*-

#Goal: From the converted text separate out the objects

import pdftotext
class Proposal:
    def __init__(self):
        self.action = "";
        self.object = "";
        self.description = "";

class ProposalMachine:
    ## The Proposal Machine Works as follows:
    #   stage 0 : Search for the first Word of a line to be the ACTION. Add the action to current proposal
    #   add the rest of the line to object of current Proposal
    #   stage 1: Next line, Search for either an action word, then all caps. If an action word, Create secondary proposal,
    # if all caps, add line to current proposals object. if neither, move to stage 3
    #stage 2 : if the first word in the description is a "A.", go into multiple description mode.
    #else go until empty line;

    ##however, an issue is that multiple actions and objects may share a description.
    def __init__(self):
        self.stage = 0
        self.currentProp = [Proposal()];
        self.completedProps = [];
    def StringList(self):
        s = [];
        for prop in self.completedProps:
            currentstring = "Action: "+prop.action+"; Object: "+prop.object+"; description:"+prop.description
            s.append(currentstring)
        return s
    def addDescription(self,section):
        for p in self.currentProp:
            p.description+=(" "+section);
    def process(self, section):
        working_section = section;
        if(self.stage == 0):
            self.stage0(working_section)
        elif(self.stage == 1):
            self.stage1(working_section)
        else:
            self.stage = 0;
            for p in self.currentProp:
                self.completedProps.append(p);
            self.currentProp = [Proposal()]

    def stage0(self,section):
        firstWord = section.split(" ")[0]
        if(firstWord=="ESTABLISH" or firstWord == "RESCIND"):
            self.currentProp[-1].action = firstWord
            self.currentProp[-1].object = section.split("–")[1];
            self.stage = 1;
    def stage1(self,section):
        firstWord = section.split(" ")[0]
        if(firstWord=="ESTABLISH" or firstWord == "RESCIND"):
            self.currentProp.append(Proposal())
            self.currentProp[-1].action = firstWord
            self.currentProp[-1].object = section.split("–")[1]
        elif(firstWord.isupper()):
            self.currentProp[-1].object+=(" "+section)
        else:
            self.addDescription(section)
            self.stage = 2;



def main():
    text = pdftotext.convert_pdf_to_txt("Engineering_Public_Hearing_example.pdf")
    sections = text.split("\n")
    count = 0;
    pmachine = ProposalMachine()
    for sect in sections:
        pmachine.process(sect)
        print(pmachine.StringList());
    print("final count"+str(len(pmachine.completedProps)))

if __name__ == '__main__':
    main()
