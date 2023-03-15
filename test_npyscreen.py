import npyscreen
#import tree_model 
#from tree_model import tree

class Form(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)
    
    def create(self):
        self.list = self.add(npyscreen.MultiLineEdit, name='multiline', value='hello\nhello')

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', Form, name='Tree_2_Do')

if __name__ == '__main__':
    TestApp = MyApplication().run()
    print('hello')