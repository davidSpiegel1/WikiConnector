// wxWidgets "Hello world" Program
// For compilers that support precompilation, includes "wx/wx.h".
#include <wx/wxprec.h>
#include <wx/notebook.h>
#ifndef WX_PRECOMP
    #include <wx/wx.h>
#endif
// For file input/output
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
//#include <wx/osx/core/cfstring.h>
//#include <wx/osx/core/cfref.h>
#include <wx/taskbar.h>
#include <wx/image.h>
#include <vector>

// Attempting to include the controller
#include "../controller/Controller.h"

std::string getOsName()
{
    #ifdef _WIN32
    return "Windows 32-bit";
    #elif _WIN64
    return "Windows 64-bit";
    #elif __APPLE__ || __MACH__
    return "Mac OSX";
    #elif __linux__
    return "Linux";
    #elif __FreeBSD__
    return "FreeBSD";
    #elif __unix || __unix__
    return "Unix";
    #else
    return "Other";
    #endif
} 

using namespace std;

//class MyFrame;
// Apparently going to have to make a custom MyTaskBarIcon in order to add an action listener
// this sucks..
class MyTaskBarIcon : public wxTaskBarIcon{
	public: 
		wxWindow * parFrame;
		MyTaskBarIcon(wxWindow * parFrame) {
			this->parFrame = parFrame;
		};

	//void OnLeftButtonDClick(wxTaskBarIconEvent&);
	//void OnMenuRestore(wxCommandEvent&);
	//void OnMenuExit(wxCommandEvent&);

	//virtual wxMenu * CreatePopupMenu() wxOVERRIDE;

	// This class handles events
	void OnLeftButtonDClick(wxTaskBarIconEvent&); 
    	void OnMenuRestore(wxCommandEvent&); 
    	void OnMenuExit(wxCommandEvent&); 
      	virtual wxMenu *CreatePopupMenu(); 
	DECLARE_EVENT_TABLE()
};

enum {
    PU_RESTORE = 10001,
    PU_EXIT,
};


class MyApp: public wxApp
{
public:
    virtual bool OnInit();
};
class MyFrame: public wxFrame
{
public:
    MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size);
private:
    void OnHello(wxCommandEvent& event);
    void OnConnect(wxCommandEvent& event);
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
    void OnButtonClick(wxCommandEvent& event);
    void OnConnectClick(wxCommandEvent& event);
    void OnConnectClickStr(string str);
    void OnConnectorPick(wxCommandEvent& event);
    void ExcelViewer(wxCommandEvent& event);
    //void OnClick2(wxTaskBarIconEvent& event);
    //wxDECLARE_EVENT_TABLE();

    wxNotebook * notebook; // Kinda like a notebook instance variable
    wxTextCtrl * textBox;    // Going to try and do this for text box as well
    wxPanel * videoPanel; // Need a video panel for the result.
    //MyFrame * frame; // Need the itital frame
    wxMenu * menuConnect;
    MyTaskBarIcon * m_taskBarIcon;
    Controller  controller;
    //string connectionManagers[2] = {"Wiki","WorldBank"};

    vector<string> connectors;
    //connectors.push_back(myString);

    vector<string>  connectionManagers;
    vector<int> connectionIds;
    vector<int> myIds;
    //connectionManagers.push_back(myString);
    //connectionManagers.push_back("WorldBank");

    wxDECLARE_EVENT_TABLE();
};
enum
{
    ID_Hello = 1,
    ID_ADD_CONNECT = 2,
    ID_CONNECT = 3	    
};

// Defining the event table
wxBEGIN_EVENT_TABLE(MyFrame, wxFrame)
    EVT_MENU(ID_Hello,   MyFrame::OnHello)
    EVT_MENU(ID_ADD_CONNECT,MyFrame::OnConnect)
    EVT_MENU(wxID_ANY,MyFrame::OnConnectorPick)
    EVT_MENU(wxID_EXIT,  MyFrame::OnExit)
    EVT_MENU(wxID_ABOUT, MyFrame::OnAbout)
wxEND_EVENT_TABLE()

// Event table for MyTaskBarIcon
BEGIN_EVENT_TABLE( MyTaskBarIcon, wxTaskBarIcon)
    EVT_MENU(PU_RESTORE, MyTaskBarIcon::OnMenuRestore)
    EVT_MENU(PU_EXIT,    MyTaskBarIcon::OnMenuExit)
    EVT_TASKBAR_LEFT_DCLICK  (MyTaskBarIcon::OnLeftButtonDClick)
END_EVENT_TABLE()



// Functions for MyTaskBarIcon from the contextual 
void MyTaskBarIcon::OnMenuRestore(wxCommandEvent& ) // Maximise program
{
    parFrame->Show(true);
}

void MyTaskBarIcon::OnMenuExit(wxCommandEvent& ) // Exit Function
{
    parFrame->Close(true);
}

void MyTaskBarIcon::OnLeftButtonDClick(wxTaskBarIconEvent&) // Maximise program again
{
    parFrame->Show(true);
}

// Pop up menu for the TaskBarIcon
wxMenu *MyTaskBarIcon::CreatePopupMenu()
{
	
    if (parFrame->IsShown()){
    	parFrame->Show(false);
    }else{
	parFrame->Show(true);
    }
    //wxMenu *menu = new wxMenu;
    
    //menu->Append(PU_RESTORE, _T("&Restore Q.S.S"));
    //menu->Append(PU_EXIT,    _T("E&xit"));

    return NULL;
}


wxIMPLEMENT_APP(MyApp);


MyTaskBarIcon * CreateMenuBarIcon(MyFrame * f){
  // Create the status item
   wxImage image(wxT("icon4.png"),wxBITMAP_TYPE_PNG);
   
   MyTaskBarIcon * icon; 
   if (image.IsOk()) // Check if the image loaded successfully
   {
    wxIcon sample;
    sample.CopyFromBitmap(wxBitmap(image));
    
    icon = new MyTaskBarIcon(f);

    icon->SetIcon(sample);

   }

    return icon;
}

bool MyApp::OnInit()
{
    
	// WILL DO THIS on clicking the icon!!
	int y = 20;
	wxSize screenSize = wxGetDisplaySize();
	int x = screenSize.GetWidth()-600;
	MyFrame * frame = new MyFrame( "Embedded Connector", wxPoint(x,y), wxSize(350, 250));
    	//wxFrame * frame = new wxFrame(NULL,wxID_ANY,"Blah",wxDefaultPosition,wxSize(100,100));
	if ("Mac OSX" == getOsName() || "Linux" == getOsName()){
		frame->Show(false);
	}else{
		frame->Show(true);
	}
    return true;
}




// MyFrame
MyFrame::MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size)
        : wxFrame(NULL, wxID_ANY, title, pos, size)
{

	// Initalizing the connectors and connection managers
    connectors.push_back("Wiki");

    connectionManagers.push_back("Wiki");
    connectionManagers.push_back("WorldBank");
    connectionManagers.push_back("AppleMusic");

    connectionIds.push_back(5);// Id for Wiki is 5
    connectionIds.push_back(6); // Id for WorldBank is 6
    connectionIds.push_back(7); // Id for AppleMusic is 7

    myIds.push_back(5);

    std::cout << getOsName();
    wxMenu *menuFile = new wxMenu;
    menuFile->Append(ID_Hello, "&Hello...\tCtrl-H",
                     "Help string shown in status bar for this menu item");
    menuFile->AppendSeparator();
    menuFile->Append(wxID_EXIT);

    // The menu help button
    wxMenu *menuHelp = new wxMenu;
    menuHelp->Append(wxID_ABOUT);

    // The menu 
     menuConnect = new wxMenu;
    for (int i=0;i<=connectors.size()-1;i++){
	    //int number = std::stoi(connectors.at(i));
	    
	    wxMenuItem * buttonItem = new wxMenuItem(menuConnect,i+5,connectors.at(i),"", wxITEM_NORMAL);
	    buttonItem->SetHelp(std::to_string(i+5));
	    //Bind(wxEVT_COMMAND_MENU_SELECTED,&MyFrame::OnConnectClick,this,i+5,buttonItem->GetId());
	    Bind(wxEVT_COMMAND_MENU_SELECTED,[=](wxCommandEvent &e){

			wxMessageBox("Button clicked",buttonItem->GetHelp(),wxOK | wxICON_INFORMATION);

			OnConnectClickStr(buttonItem->GetHelp().mb_str().data());

	    },buttonItem->GetId());
	    menuConnect->Append(buttonItem);
	    //Bind(wxEVT_COMMAND_MENU_SELECTED,&MyFrame::OnConnectClick,this,i+5,buttonItem->GetId());//,i+5/*buttonItem->GetId()*/);
	    
	    
	    //menuConnect->Append(wxID_ANY,connectors.at(i),"Connetor Name");
	

    }
    menuConnect->Append(ID_ADD_CONNECT, "&Add Connector... \tCtrl-H","Add a connector to query");
    //Bind(wxEVT_COMMAND_MENU_SELECTED,&MyFrame::OnConnect,ID_ADD_CONNECT);

    // The menu bar object that is seen when app is clicked
    wxMenuBar *menuBar = new wxMenuBar;

    // Append the task bar buttons
    menuBar->Append( menuFile, "&File" );
    menuBar->Append( menuHelp, "&Help" );
    menuBar->Append( menuConnect, "&Connectors" );
    SetMenuBar( menuBar );
    CreateStatusBar();
    SetStatusText( "Welcome to wxWidgets!" );

    if ("Mac OSX"==getOsName() || "Linux" == getOsName()){  
	//Controller controller;
	//cout << controller.getConnector(); 
    	wxInitAllImageHandlers();
    	m_taskBarIcon = CreateMenuBarIcon(this); 
    }
    // Okay, now I am going to try to create a notebook
    notebook = new wxNotebook(this,wxID_ANY, wxDefaultPosition, wxDefaultSize, 0, "MyNotebook");

    // Add pages to the notebook
    //notebook->AddPage(new wxPanel(notebook),"Video");
    videoPanel = new wxPanel(notebook);
    videoPanel->SetBackgroundColour(wxColour(73,73,73));
    notebook->AddPage(videoPanel,"Video");
    wxPanel* blackPanel = new wxPanel(notebook);

    // Going to attempt to place data inside the black panel
    wxButton* button = new wxButton(blackPanel,wxID_ANY, "Q", wxDefaultPosition, wxDefaultSize);
    textBox = new wxTextCtrl(blackPanel, wxID_ANY, "", wxDefaultPosition, wxSize(130,25), wxTE_MULTILINE);


    textBox->SetForegroundColour(wxColour(208,208,208));
    textBox->SetBackgroundColour(wxColour(73,73,73));

    button->Bind(wxEVT_BUTTON,&MyFrame::OnButtonClick,this);
    // Add a sizer to center the text box
    wxBoxSizer* panelSizer = new wxBoxSizer(wxVERTICAL);
    panelSizer->AddStretchSpacer();
    panelSizer->Add(textBox, 0, wxALIGN_CENTER | wxALL, 10);
    panelSizer->Add(button,0,wxALIGN_CENTER | wxALL, 5);
    panelSizer->AddStretchSpacer();
    blackPanel->SetSizerAndFit(panelSizer);


    blackPanel->SetBackgroundColour(wxColour(73, 73, 73)); 
    notebook->AddPage(blackPanel,"Query");

    notebook->ChangeSelection(1);
    // Center the frame on the screen
    SetPosition(pos);
    SetSize(size);
   // Centre();
}; // I think you need this 
void MyFrame::OnExit(wxCommandEvent& event)
{
    Close( true );
}
void MyFrame::OnAbout(wxCommandEvent& event)
{
    wxMessageBox( "This is an app that ",
                  "About Hello World", wxOK | wxICON_INFORMATION );
}
void MyFrame::OnHello(wxCommandEvent& event)
{
    wxLogMessage("Video Connector");
}

void MyFrame::OnConnect(wxCommandEvent& event){

	wxMessageBox("Connect MarketPlace clicked","About", wxOK | wxICON_INFORMATION);
	//Show(false);
	int y = 20;
	wxSize screenSize = wxGetDisplaySize();
	int x = screenSize.GetWidth()-600;
	wxFrame * f = new wxFrame(NULL,wxID_ANY,"Connector MarketPlace",wxPoint(x,y),wxSize(400,250));
	
	// A panel
	//wxPanel * panel = new wxPanel();
	// The list of possible connecto
	wxSizer * sizer = new wxBoxSizer(wxVERTICAL);
	wxScrolledWindow * sw = new wxScrolledWindow(f, wxID_ANY,wxPoint(0,0),wxSize(350,200));
	int x1 = 50;
	int x2 = 50;
	for (int i = 0; i<= connectionManagers.size()-1;i++){
		//wxButton * b1 = new wxButton(sw,wxID_ANY,connectionManagers.at(i),wxPoint(x1,x2),wxDefaultSize);
		//b1->SetName(connectionManagers.at(i));
		//b1->Bind(wxEVT_BUTTON, &MyFrame::OnConnectorPick,this);
		
		wxCheckBox * cbox = new wxCheckBox(sw,wxID_ANY,connectionManagers.at(i),wxPoint(x1,x2),wxDefaultSize);
		cbox->SetName(connectionManagers.at(i));
		//cbox->Bind(wxEVT_BUTTON,&MyFrame::OnConnectorPick,this);
		cbox->Bind(wxEVT_CHECKBOX,[this,cbox](wxCommandEvent& event){
			
			wxMessageBox("HI",cbox->GetName(),wxOK);
			if (cbox->GetName()=="Wiki"){

				connectors.push_back("Wiki");
				myIds.push_back(5);

			}else if (cbox->GetName()=="WorldBank"){

				connectors.push_back("WorldBank");
				myIds.push_back(6);

			}else if (cbox->GetName()=="AppleMusic"){

				connectors.push_back("AppleMusic");
				myIds.push_back(7);

			}else{

				
			}
		});

		if (i <= connectors.size()-1){
			int c = count(connectors.begin(),connectors.end(),connectors.at(i));
		if (c >= 1){
			//	b1->Enable(false);
			cbox->SetValue(false);
		}
		}
		x2 = x2+50;
	}
	wxBoxSizer * wdSizer = new wxBoxSizer(wxVERTICAL);
	wdSizer->Add(sizer,0,wxALIGN_CENTER,2);
	sw->SetSizer(wdSizer);

	
	wxTextCtrl * textBox = new wxTextCtrl(f, wxID_ANY, "Default Name", wxPoint(100,0), wxSize(130,25), wxTE_MULTILINE);

	wxButton * done = new wxButton(f,wxID_ANY,"DONE?",wxPoint(x2+10,x1+10),wxSize(100,100));
	sw->FitInside();
	sw->SetScrollRate(3,3);


	done->Bind(wxEVT_BUTTON,[=](wxCommandEvent &e){
	
		
			wxMessageBox("WHAT",connectors.back(), wxOK);


		if (textBox->GetValue() != "Default Name"){

			
			wxMenuItem * it = new wxMenuItem(menuConnect,6,textBox->GetValue());

			
			it->SetHelp(std::to_string(myIds.back()));
			//Bind(wxEVT_COMMAND_MENU_SELECTED,&MyFrame::OnConnectClick,this /*,it->GetHelp()*/);

			 Bind(wxEVT_COMMAND_MENU_SELECTED,[=](wxCommandEvent &e){

			wxMessageBox("Button clicked",it->GetHelp(),wxOK | wxICON_INFORMATION);

			OnConnectClickStr(it->GetHelp().mb_str().data());

	    },it->GetId());
			wxMenuItem * item = menuConnect->FindItem(ID_ADD_CONNECT);
			

			menuConnect->Delete(item);

			menuConnect->Append(it);
			menuConnect->Append(ID_ADD_CONNECT, "&Add Connector... \tCtrl-H","Add a connector to query");


		}
	
		f->Close();


	});

	f->Show(true);
	
}


void MyFrame::OnConnectorPick(wxCommandEvent& event){

	auto  * btn = (wxCheckBox *) event.GetEventObject();
	wxMessageBox("WHAT",btn->GetName(), wxOK);
	if (btn->GetName() == "Wiki"){
	
		int c = count(myIds.begin(),myIds.end(),5);
	   if (c <= 0){
		
		connectors.push_back("Wiki");
		myIds.push_back(5);
		
		btn->Enable(false);
	   }

	}else if (btn->GetName() == "WorldBank"){
		int c = count(myIds.begin(),myIds.end(),6);	
	   if (c <= 0){
		connectors.push_back("WorldBank");
		myIds.push_back(6);
		//wxMenuItem * it2 = new wxMenuItem(menuConnect,wxID_ANY,"WorldBank");
		//menuConnect->Append(it2);
		//btn->Enable(false);
	   }	
		

	}else if (btn->GetName() == "AppleMusic"){
			int c = count(myIds.begin(),myIds.end(),6);
		if (c <= 0){
			connectors.push_back("AppleMusic");
			myIds.push_back(7);
		}
	}
	//wxString str = wxString(std::to_string(event.GetName()));

}

void MyFrame::OnConnectClick(wxCommandEvent& event){
	//wxString str = wxString(std::to_string(event.GetHelp()));

	auto * btn = (wxMenuItem *) event.GetEventObject();

	wxString str = wxString(btn->GetHelp());
	wxString str2 = wxString(std::to_string(btn->GetId()));	
	if (str=="5"){
		controller.changeConnector("Wiki");

	}else if (str=="6"){

		controller.changeConnector("WorldBank");
	}else if (str=="7"){
	
		controller.changeConnector("AppleMusic");
	}else
	{
		wxMessageBox("Not right but"+str,str2,wxOK);

	}


}


void MyFrame::OnConnectClickStr(string str){

 	wxString str2 = wxString(str);
	if (str=="5"){
		controller.changeConnector("Wiki");
	} else if (str=="6"){

		controller.changeConnector("WorldBank");
	} else if (str=="7"){

		controller.changeConnector("AppleMusic");
	}

	else{
		wxMessageBox("Not right button",str2,wxOK);
	}

}	

// What happends when button is clicked
void MyFrame::OnButtonClick(wxCommandEvent& event){



	wxMessageBox("Button clicked",textBox->GetValue(),wxOK | wxICON_INFORMATION);
	videoPanel->DestroyChildren();
	

	notebook->ChangeSelection(0);
	
	// Attempting to pass the data to the controller
	std::string query = std::string(textBox->GetValue().ToStdString());
	controller.Query(query);


	std::ifstream myfile("test.csv");
	//myfile.open("test.csv");
	std::string str;
	std::string title = "TITLE:";
	std::string pageid = "PAGEID:";
	size_t pos = 0;
	size_t pos2 = 0;
	int posX = 10;
	int posY = 10;
	int sizeX = 300;
	int sizeY = 50;
	int count = 1;
	
	wxSizer * sizer = new wxBoxSizer(wxVERTICAL);
	wxScrolledWindow * wd = new wxScrolledWindow(videoPanel,wxID_ANY,wxPoint(0,0),wxSize(345,245));
	
	while (std::getline(myfile,str)){
		
		bool isFound = (pos=str.find(title)) != std::string::npos;
		bool isFound2 = (pos2=str.find(pageid)) != std::string::npos;

		if (isFound && isFound2){
			// TITLE
			std::string newStr = str.substr(pos+6,pos2-7);
			wxButton * bn = new wxButton(wd,wxID_ANY,newStr,wxPoint(posX,posY),wxSize(sizeX,sizeY));
			
			bn->SetName(newStr);
			
			bn->Bind(wxEVT_BUTTON,&MyFrame::ExcelViewer,this);
			
			sizer->Add(bn,0,wxALIGN_CENTER,2);	

			//osX = posX+100;
			//if (count%2 == 0){
				posY = posY+10;
			//	posX = 0;
			//}
		}// End of isFound
		count++;
	}// End of while
	 
	//wxScrolledWindow * wd = new wxScrolledWindow(videoPanel,wxID_ANY);

	wxBoxSizer * wdSizer = new wxBoxSizer(wxVERTICAL);
	wdSizer->Add(sizer,0,wxALIGN_CENTER,2);
	wd->SetSizer(wdSizer);
	wd->FitInside();
	wd->SetScrollRate(3,3);

}

void MyFrame::ExcelViewer(wxCommandEvent& event){

	int y = 20;
	wxSize screenSize = wxGetDisplaySize();
	int x = screenSize.GetWidth()-600;
	wxFrame * f = new wxFrame(NULL,wxID_ANY,"Excel Viewer",wxPoint(x,y),wxSize(400,250));

	f->Show(true);

}
		
