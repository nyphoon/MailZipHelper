#!/usr/bin/env python
# modified from example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

import urllib

import zip_cx
TARGET_TYPE_URI_LIST = 80
dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]

class MailZipHelper:

    # modified from http://faq.pygtk.org/index.py?req=show&file=faq23.031.htp
    def get_file_path_from_dnd_dropped_uri(self, uri):
        # get the path to file
        if uri.startswith('file:\\\\\\'): # windows
            path = uri[8:] # 8 is len('file:///')
        elif uri.startswith('file://'): # nautilus, rox
            path = uri[7:] # 7 is len('file://')
        elif uri.startswith('file:'): # xffm
            path = uri[5:] # 5 is len('file:')
        else:
            path = ""

        path = urllib.url2pathname(path) # escape special chars
        path = path.strip('\r\n\x00') # remove \r\n and NULL

        return path

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        uri = selection.data.strip('\r\n\x00')
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = self.get_file_path_from_dnd_dropped_uri(uri)
            zip_cx.zip_create(path)
            # if os.path.isfile(path): # is it file?
            #     data = file(path).read()
            #     print data

    def cb_btn_add(self, widget, data=None):
        print "Add"
    def cb_btn_clean(self, widget, data=None):
        print "Clean"
    # ref: pyGTK org helloworld sample
    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def cb_btn_create(self, widget, data=None):
        print "Create"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(320,320)
        self.window.set_title('Mail Zip Helper')
        self.window.drag_dest_set( gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
            dnd_list, gtk.gdk.ACTION_DEFAULT)

        self.window.connect("drag_data_received", self.on_drag_data_received)
        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)
    
        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        self.window.set_border_width(10)
        
        # create box to pack widgets. make UI layout.
        # Put box_input in window. There are 3 horizon box in this box_input.
        self.box_input = gtk.VBox(False, 0)
        self.box_input_h1 = gtk.HBox(False, 0)
        self.box_input_h2 = gtk.HBox(False, 0)
        self.box_input_h3 = gtk.HBox(False, 0)
        self.box_input.pack_start(self.box_input_h1, False, False, 0)
        self.box_input.pack_start(self.box_input_h2, False, False, 0)
        self.box_input.pack_start(self.box_input_h3, False, False, 0)
        self.window.add(self.box_input)
        
        # button [Add]
        self.btn_add = gtk.Button("Add")
        self.btn_add.connect("clicked", self.cb_btn_add, None)
        self.btn_add.show()
        self.box_input_h1.pack_start(self.btn_add, False, False, 0)
        
        # button [Clean]
        self.btn_clean = gtk.Button("Clean")
        self.btn_clean.connect("clicked", self.cb_btn_clean, None)
        self.btn_clean.show()
        self.box_input_h1.pack_start(self.btn_clean, False, False, 0)
        
        # button [Create]
        self.btn_create = gtk.Button("Create")
        self.btn_create.connect("clicked", self.cb_btn_create, None)
        self.window.add(self.btn_create)
        self.btn_create.show()
        self.box_input_h3.pack_start(self.btn_create, False, False, 0)
        
        # item list
        listitem = gtk.ListItem('ite1')
        listitem2 = gtk.ListItem('item2')
        listitem.show()
        listitem2.show()
        items = [listitem,listitem2]
        self.list_file = gtk.List()
        self.list_file.append_items(items)
        self.list_file.set_usize(200,200)
        self.list_file.show()
        self.box_input_h2.pack_start(self.list_file, False, False, 0)
        
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.box_input.show()
        self.box_input_h1.show()
        self.box_input_h2.show()
        self.box_input_h3.show()
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    window = MailZipHelper()
    window.main()
