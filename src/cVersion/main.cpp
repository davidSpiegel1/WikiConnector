// main.cpp <- basically the app so far. Really a test.
//
#include <iostream>
#include "wx/wxprec.h"

#ifndef WX_PRECOMP
	#include "wx/wx.h"
#endif

// iDs for the menu items

enum
{
  QuitID = wxID_EXIT,
  ClearID = wxID_CLEAR

};

// So, this seems like a class definition
class MyFrame : public wxFrame
{
// Seems to be the public functions being declared
public:
	MyFrame(const wxString& title);
  

private:
	// The event handlers
	// OnQuit is the action, event is like e in java
	void OnQuit(wxCommandEvent& WXUNUSED(event)) { Close(true);}
	void OnAbout(wxCommandEvent& event);
	void OnInputWindowKind(wxCommandEvent& event);

};	
class MyApp : public wxApp
{
public:
	// This is basically the main program
	virtual bool OnInit() wxOVERRIDE
	{
		// Basically the frame class we made (Note this is a wxFrame type)
		new MyFrame("Keyboard wxWidgets App");
		return true;
	}
};

wxIMPLEMENT_APP(MyApp); // This will 'run' the app

MyFrame::MyFrame(const wxString& title) : wxFrame(NULL,wxID_ANY,title),
					m_inputWin(NULL),
					m_skipHook(true),
					m_skipDown(true)
{
	//SetIcon(wxICON(sample));
	wxMenu *menuFile = new wxMenu;
