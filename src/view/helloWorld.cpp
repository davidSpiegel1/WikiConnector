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
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
    void OnButtonClick(wxCommandEvent& event);
    //void OnClick2(wxTaskBarIconEvent& event);
    //wxDECLARE_EVENT_TABLE();

    wxNotebook * notebook; // Kinda like a notebook instance variable
    wxTextCtrl * textBox;    // Going to try and do this for text box as well
    wxPanel * videoPanel; // Need a video panel for the result.
    //MyFrame * frame; // Need the itital frame
    MyTaskBarIcon * m_taskBarIcon;

    wxDECLARE_EVENT_TABLE();
};
enum
{
    ID_Hello = 1
};

// Defining the event table
wxBEGIN_EVENT_TABLE(MyFrame, wxFrame)
    EVT_MENU(ID_Hello,   MyFrame::OnHello)
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


//wxDECLARE_APP(MyApp);
wxIMPLEMENT_APP(MyApp);


MyTaskBarIcon * CreateMenuBarIcon(MyFrame * f){
  // Create the status item
  //
  //
   wxImage image(wxT("icon4.png"),wxBITMAP_TYPE_PNG);
   
   MyTaskBarIcon * icon; 
   if (image.IsOk()) // Check if the image loaded successfully
   {
    wxIcon sample;
    sample.CopyFromBitmap(wxBitmap(image));
    
    icon = new MyTaskBarIcon(f);

   // icon->Connect(wxEVT_TASKBAR_LEFT_UP,wxEventHandler(MyFrame::OnTaskBarIconClick),nullptr,this);
    //wxMenu * menu = new wxMenu;
    //menu->Append(wxID_ANY, "Open Frame");
    //menu->Append(wxID_ANY, "Exit");
    //icon->Bind(wxEVT_TASKBAR_RIGHT_DOWN, &MyTaskBarIcon::OnRightClick, icon);
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
	if ("Mac OSX" == getOsName()){
		frame->Show(false);
	}else{
		frame->Show( true);
	}
    return true;
}




// MyFrame
MyFrame::MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size)
        : wxFrame(NULL, wxID_ANY, title, pos, size)
{

    std::cout << getOsName();
    wxMenu *menuFile = new wxMenu;
    menuFile->Append(ID_Hello, "&Hello...\tCtrl-H",
                     "Help string shown in status bar for this menu item");
    menuFile->AppendSeparator();
    menuFile->Append(wxID_EXIT);
    wxMenu *menuHelp = new wxMenu;
    menuHelp->Append(wxID_ABOUT);
    wxMenuBar *menuBar = new wxMenuBar;
    menuBar->Append( menuFile, "&File" );
    menuBar->Append( menuHelp, "&Help" );
    SetMenuBar( menuBar );
    CreateStatusBar();
    SetStatusText( "Welcome to wxWidgets!" );

    if ("Mac OSX"==getOsName()){   
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

// What happends when button is clicked
void MyFrame::OnButtonClick(wxCommandEvent& event){



	wxMessageBox("Button clicked",textBox->GetValue(),wxOK | wxICON_INFORMATION);
	//notebook->DeletePage(1);
	//notebook->DeletePage(0);
	videoPanel->DestroyChildren();
	

	notebook->ChangeSelection(0);
	
	// Attempting to place the query into a new file
	//std::ofstream outputFile("test.txt");
	
	int result = system("cd ..; cd model; python3 WikiSource.py "+textBox->GetValue());
	
	// Going to try and move the file into the correct drectory
	int result2 = system("cd ..; cd model; cp test.csv ../view");
	
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
	 //this->SetSizer(sizer);
	 //this->FitInside();
	 //this->SetScrollRate(5,5);
	 //sizer->FitInside(videoPanel);
	 //videoPanel->ScrollWindow(20,0);
	 /*
		if (std::getline(myfile,myline)){

			std::string delimiter = ",";
			size_t pos = 0;
		// Where we are trying to build the video panel
		while ((pos =myline.find(delimiter)) != std::string::npos){
					
			token = myline.substr(0,pos-1);
			myline.erase(0,pos+delimiter.length());
			std::string title = "TITLE:";
			
		*/	



}
