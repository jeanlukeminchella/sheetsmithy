import globalFunctions as gf
import newEntry as ne

fileExtension = ".json"
standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"



class Block():
    
    def __init__(self, entries=[], title="",divID=""):
        self.entries = entries
        self.title=title
        self.divID=divID
    
    def addEntry(self, e):
        self.entries.append(e)
        
    def getHTML(self,c=None):
        
        result = ""
        if self.title !="":
            result += "<div id='sectionTitle' class='header'>"+self.title+"</div>\n"
            
        if self.divID !="":
            result += "<div id='"+self.divID+"'>\n"
            
        for e in self.entries:
            #surely there is another way?
            if "Entry" in str(type(e)):

                result += e.getHTML(c)
            else:
                result += ne.getHTML(e,c)
        
        if self.divID !="":
            result += "</div>\n"
        
        return result
        

    
   
