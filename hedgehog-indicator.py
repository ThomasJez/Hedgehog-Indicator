#!/usr/bin/env python3

import os
import gi
import time
import db
from threading import Thread
import config

# We have to require the versions before the import
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject, GLib, Gio


class Indicator:
    """
    A Mate indicator for the third party Hamster application
    initializes a Mate indicator with time label and a menu
    """
    def __init__(self):
        self.app = 'hedgehog_indicator'
        path = os.path.dirname(os.path.abspath(__file__))
        iconpath = path + "/jez.png"
        self.indicator = AppIndicator3.Indicator.new(self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(db.get_label(), self.app)

        self.update = Thread(target=self.update_label)
        # daemonize the thread to make the indicator stoppable
        self.update.daemon = True
        self.update.start()

    @staticmethod
    def hamster_native_app(widget):
        """calls the Hamster application"""
        os.system('python3 ' + config.hamster_path)

    def create_menu(self):
        """builds a GTK menu consisting of a button for the Hamster Application and a Quit button"""
        menu = Gtk.Menu()

        item_overview = Gtk.MenuItem(label='Hamster App')
        item_overview.connect('activate', self.hamster_native_app)
        menu.append(item_overview)
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', Gtk.main_quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def update_label(self):
        """
        gets the label text from the dabase and sets it in the indcator
        has to run in a separate thread
        """
        while True:
            # the child thread updates the indicator text which runs in the main thread
            # GLib.idle_add ensures that this happens smoothly
            # https://pygobject.readthedocs.io/en/latest/guide/threading.html
            GLib.idle_add(self.indicator.set_label, db.get_label(), self.app, priority=GLib.PRIORITY_DEFAULT)
            time.sleep(1)


Indicator()
Gtk.main()
