#!/usr/bin/env python
# modified from example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

import urllib
import os
import time

import zip_cx
TARGET_TYPE_URI_LIST = 80
dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]

xpm_data = [
"32 32 3 1",
"       c None",
".      c #222222222222",
"X      c #EEEEEEEEEEEE",
"                                ",
"  ................              ",
"  .            ..               ",
"  .           ..                ",
"  .          ..                 ",
"  .         ..                  ",
"  .          ..                 ",
"  .           ..                ",
"  .            ..               ",
"  .    .        ..              ",
"  .   ...        ..             ",
"  .  .. ..        ..            ",
"  . ..   ..        ..           ",
"  ...     ..        ..          ",
"  ..       ..        ..         ",
"  .         ..                  ",
"             ..                 ",
"              ..                ",
"               ..               ",
"                ..  ......      ",
"                    .XXX.X.     ",
"                    .XXX.XX.    ",
"                    .XXX.XXX.   ",
"                    .XXX.....   ",
"                    .XXXXXXX.   ",
"                    .XXXXXXX.   ",
"                    .XXXXXXX.   ",
"                    .XXXXXXX.   ",
"                    .XXXXXXX.   ",
"                    .........   ",
"                                ",
"                                "
]

class MailZipHelper:
    file_dict = {}
    
    def file_clear(self):
        #data
        self.file_dict.clear()
        #UI
        self.liststore.clear()
        self.treeview.hide()
        self.box_input_indication.show_all()
        self.box_input_h2.show()
        self.box_input_h3.hide_all()
        self.box_input_h4.hide_all()

    def file_add(self, path):
        basename = os.path.basename(path)
        # same file name cannot be in the same root folder
        if basename in self.file_dict:
            # to do: warning message
            print('same file name')
            return
        #data
        self.file_dict[basename] = path
        self.output_name = basename+'.zip.'+time.strftime('%Y%m%d')+'nopwd'
        #UI
        self.box_input_indication.hide_all()
        model = self.treeview.get_model()
        model.append([str(len(model)+1), basename])
        self.treeview.show()
        
        # self.etr_output_name.set_flags(gtk.CAN_FOCUS)
        # self.etr_output_name.grab_focus()
        # self.etr_output_name.set_visibility(True)
        # self.etr_output_name.set_editable(True)
        # self.etr_output_name.set_text(basename+'.zip.'+time.strftime('%Y%m%d'))
        # self.etr_output_name.select_region(0, len(basename))
        
        self.lbl_output_name.set_text('Zip to: '+self.output_name)
        self.box_input_h3.show_all()
        self.box_input_h4.show_all()
        
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
            self.file_add(path)
        
    def cb_btn_add(self, widget, data=None):
        print "Add"
        # to do: filechooserdialog
        
    def cb_btn_clear(self, widget, data=None):
        print "clear"
        self.file_clear()
    def cb_btn_create(self, widget, data=None):
        print "Create"
        # zipfile = zip_cx.ZipCreate(self.etr_output_name.get_text())
        zipfile = zip_cx.ZipCreate(self.output_name)
        for path in self.file_dict:
            print('zip write: {}'.format(self.file_dict[path]))
            zipfile.write(self.file_dict[path])
        zipfile.finish()

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
        self.window.set_title('Mail Zip Helper')
        self.window.set_resizable(False)
        
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
        self.box_input.set_usize(320,320)
        self.window.add(self.box_input)
        
        self.box_input_h1 = gtk.HBox(False, 0)
        self.box_input_h1.set_usize(320,40)
        self.box_input_h2 = gtk.HBox(False, 0)
        self.box_input_h2.set_usize(320,240)
        self.box_input_h3 = gtk.HBox(False, 0)
        self.box_input_h3.set_usize(320,40)
        self.box_input_h4 = gtk.HBox(False, 0)
        self.box_input_h4.set_usize(320,40)
        self.box_input.pack_start(self.box_input_h1, False, False, 0)
        self.box_input.pack_start(self.box_input_h2, False, False, 0)
        self.box_input.pack_start(self.box_input_h3, False, False, 0)
        self.box_input.pack_start(self.box_input_h4, False, False, 0)
        
        # @ horizon 1
        # button [Add]
        self.btn_add = gtk.Button("Add")
        self.btn_add.connect("clicked", self.cb_btn_add, None)
        self.btn_add.show()
        # self.btn_add = gtk.FileChooserButton ('Add')
        # self.btn_add.connect("file-set", self.callback, None)
        self.box_input_h1.pack_start(self.btn_add, True, True, 0)
        
        # @ horizon 2
        # treeview (file list)
        self.liststore = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.liststore)
        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()
        self.tvcolumn = gtk.TreeViewColumn('#', self.cell, text=0)
        self.tvcolumn1 = gtk.TreeViewColumn('File', self.cell1, text=1)
        self.treeview.append_column(self.tvcolumn)
        self.treeview.append_column(self.tvcolumn1)
        self.treeview.set_search_column(1)
        self.box_input_h2.pack_start(self.treeview, True, True, 0)
        
        # set horizon 2 handle DnD
        self.box_input_h2.drag_dest_set( gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | 
                                    gtk.DEST_DEFAULT_DROP, dnd_list, gtk.gdk.ACTION_DEFAULT)
        self.box_input_h2.connect("drag_data_received", self.on_drag_data_received)
        
        # indication
        self.box_input_indication = gtk.VBox(False, 0)
        self.box_input_h2.pack_start(self.box_input_indication, False, False, 0)
        # - picture
        pbuf = gtk.gdk.pixbuf_new_from_xpm_data(xpm_data)
        new = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 32*6,32*6 )
        pbuf.scale(new, 0,0, 32*6,32*6, 0,0, 6,6, gtk.gdk.INTERP_NEAREST)
        image = gtk.Image()
        image.set_from_pixbuf(new)
        self.box_input_indication.pack_start(image, False, False, 0)
        # - text
        label = gtk.Label()
        label.set_markup('<span size="20000">Drag&amp;Drop Your File Here</span>')
        self.box_input_indication.pack_start(label, False, False, 0)
        
        self.box_input_indication.show_all()
        
        # @ horizon 3
        # label [output_name title]
        self.lbl_output_name = gtk.Label('Zip to:')
        self.box_input_h3.pack_start(self.lbl_output_name, False, False, 0)
        # entry [output_name]
        # self.etr_output_name = gtk.Entry(max=82)
        # self.box_input_h3.pack_start(self.etr_output_name, True, True, 0)
        
        # @ horizon 4
        # button [Create]
        self.btn_create = gtk.Button("Create")
        self.btn_create.connect("clicked", self.cb_btn_create, None)
        self.box_input_h4.pack_start(self.btn_create, True, True, 0)
        # button [Clear]
        self.btn_clear = gtk.Button("Clear")
        self.btn_clear.connect("clicked", self.cb_btn_clear, None)
        self.box_input_h4.pack_start(self.btn_clear, False, False, 0)
        
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.file_clear()
        self.box_input.show()
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
