#!/usr/bin/env python3
import os
import signal
import gi

import config

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject, GLib, Gio
import time
import db
from threading import Thread

class Indicator():
    def __init__(self):
        self.app = 'hedgehog_indicator'
        path = os.path.dirname(os.path.abspath(__file__))
        iconpath = path+"/jez.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())

        self.indicator.set_label(self.get_label(), self.app)
        # the thread:
        self.update = Thread(target=self.show_seconds)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()
        self.add_monitor(config.db_path)

    def get_label(self):
        return db.get_label()

    def hamster_overview(self, widget):
        os.system('python3 ' + config.hedgehog_path + ' overview')

    def hamster_stop(self, widget):
        os.system('python3 ' + config.hedgehog_path + ' stop')

    def hamster_new(self, widget):
        os.system('python3 ' + config.hedgehog_path + ' new')

    def hamster_earlier(self, widget):
        os.system('python3 ' + config.hedgehog_path + ' earlier')

    def hamster_app(self, widget):
        os.system('python3 ' + config.hedgehog_path)

    def hamster_native_app(self, widget):
        os.system('python3 ' + config.hamster_path)

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        item_earlier = Gtk.MenuItem(label='Former Activity')
        item_earlier.connect('activate', self.hamster_earlier)
        menu.append(item_earlier)

        item_new = Gtk.MenuItem(label='New Activity')
        item_new.connect('activate', self.hamster_new)
        menu.append(item_new)

        item_stop = Gtk.MenuItem(label='Stop Current Activity')
        item_stop.connect('activate', self.hamster_stop)
        menu.append(item_stop)

        item_app = Gtk.MenuItem(label='Hedgehog App')
        item_app.connect('activate', self.hamster_app)
        menu.append(item_app)

        item_overview = Gtk.MenuItem(label='Overview')
        item_overview.connect('activate', self.hamster_overview)
        menu.append(item_overview)

        item_overview = Gtk.MenuItem(label='Hamster App')
        item_overview.connect('activate', self.hamster_native_app)
        menu.append(item_overview)

        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def show_seconds(self):
        t = 2
        while True:
            time.sleep(1)
            GLib.idle_add(
                self.indicator.set_label,
                self.get_label(), self.app,
                priority=GLib.PRIORITY_DEFAULT
            )
            t += 1

    def stop(self, source):
        Gtk.main_quit()

    def on_file_changed(self, monitor, f1, f2, evt):
        print("Changed", f1, f2, evt)
        '''
        # print(f1)
        # print(f2)
        # print(evt)
        if self.get_label() == 'Keine Tätigkeit':
            self.showmore = False
            print('Keine Tätigkeit')

        else:
            self.showmore = True
            if not self.seconds_run:
                self.seconds = Thread(target=self.show_seconds)
                self.seconds.setDaemon(True)
                self.seconds_run = True
                self.seconds.start()
        # print(len(threading.enumerate()))
        '''

    def add_monitor(self, file):
        gdir = Gio.File.new_for_path(file)
        self.monitor = gdir.monitor_file(Gio.FileMonitorFlags.NONE, None)
        self.monitor.connect("changed", self.on_file_changed)

Indicator()
# this is where we call GObject.threads_init()
#GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
