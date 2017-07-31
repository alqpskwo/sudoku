import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import puzzle
import copy
import pickle

class SudokuWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Sudoku")

        self.set_default_size(200, 200)
        self.set_hexpand(False)
        self.puz = puzzle.Puzzle()
        self.puz.generate()
        self.puz_reset = copy.deepcopy(self.puz)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.props.margin = 3
        grid = Gtk.Grid()

        self.cells = {}
        for row in range(0, 9):
            for col in range(0, 9):
                entry = SudokuEntry(row, col)
                entry.connect("changed", self.on_text_entered)
                grid.attach(entry, 1 + (row // 3) * 4 + (row % 3),
                                   1 + (col // 3) * 4 + (col % 3), 1 ,1)
                self.cells[row, col] = entry

        for col in range(0, 13, 4):
            vline = Gtk.Box()
            vline.set_size_request(2, -1)
            vline.modify_bg(0, Gdk.color_parse('black'))
            grid.attach(vline, col, 0, 1, 13)

        for row in range(0, 13, 4):
            hline = Gtk.Box()
            hline.set_size_request(-1, 2)
            hline.modify_bg(0, Gdk.color_parse('black'))
            grid.attach(hline, 0, row, 13, 1)
        vbox.pack_start(grid, False, False, 3)

        grid = Gtk.Grid()

        button = Gtk.Button.new_with_label("Check")
        button.props.hexpand = True
        button.connect("clicked", self.on_check_clicked)
        grid.attach(button, 0, 0, 1, 1)

        button = Gtk.Button.new_with_label("Solve")
        button.props.hexpand = True
        button.connect("clicked", self.on_solve_clicked)
        grid.attach(button, 1, 0, 1, 1)

        button = Gtk.Button.new_with_label("New")
        button.props.hexpand = True
        button.connect("clicked", self.on_new_clicked)
        grid.attach(button, 0, 1, 1, 1)

        button = Gtk.Button.new_with_label("Reset")
        button.props.hexpand = True
        button.connect("clicked", self.on_reset_clicked)
        grid.attach(button, 1, 1, 1, 1)

        button = Gtk.Button.new_with_label("Save")
        button.props.hexpand = True
        button.connect("clicked", self.on_save_clicked)
        grid.attach(button, 0, 2, 1, 1)

        button = Gtk.Button.new_with_label("Open")
        button.props.hexpand = True
        button.connect("clicked", self.on_open_clicked)
        grid.attach(button, 1, 2, 1, 1)

        vbox.pack_start(grid, True, True, 0)
        self.add(vbox)
        self.update()

        with open('sample', 'wb') as f:
            pickle.dump(self.puz, f)




    def on_text_entered(self, entry):
        text = entry.get_text()
        try:
            self.puz.values[entry.row, entry.col] = int(text)
        except ValueError:
            if text.isspace or not text:
                self.puz.values[entry.row, entry.col] = 0
        finally:
            if self.puz.values[entry.row, entry.col] > 0:
                entry.set_text(str(self.puz.values[entry.row, entry.col]))
            else:
                entry.set_text('')

    def on_new_clicked(self, button):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL,
            "Are you sure you want to generate a new puzzle? The current puzzle will be lost.")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            self.puz = puzzle.Puzzle()
            self.puz.generate()
            self.puz_reset = copy.deepcopy(self.puz)
            self.update()

    def on_reset_clicked(self, button):
        self.puz = copy.deepcopy(self.puz_reset)
        self.update()

    def on_check_clicked(self, button):
        try:
            puz = copy.deepcopy(self.puz)
            puz.complete()
        except puzzle.NoSolutionError:
            message = "The puzzle is incorrect."
        else:
            message = "The puzzle is correct so far."
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, message)
        dialog.run()
        dialog.destroy()

    def on_solve_clicked(self, button):
        try:
            puz = copy.deepcopy(self.puz)
            puz.complete()
            self.puz = puz
        except puzzle.NoSolutionError:
            self.error_dialog("The puzzle has no solution.")
        self.update()

    def on_save_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Choose file name and location.", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                with open(dialog.get_filename(), 'wb') as f:
                    pickle.dump( (self.puz, self.puz_reset), f)
            except (IOError, OSError, pickle.PicklingError):
                self.error_dialog("The file could not be saved.")
            dialog.destroy()


    def on_open_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Choose a file to open.", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                with open(dialog.get_filename(), 'rb') as f:
                    loaded = pickle.load(f)
                assert isinstance(loaded[0], puzzle.Puzzle)
                assert isinstance(loaded[1], puzzle.Puzzle)
            except (AssertionError, IndexError, ImportError,
                    TypeError, pickle.UnpicklingError, IOError, OSError):
                self.error_dialog("The file could not be opened.")
            else:
                self.puz, self.puz_reset = loaded
        dialog.destroy()
        self.update()

    def update(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if self.puz.values[row, col] > 0:
                    self.cells[row, col].set_text(str(self.puz.values[row, col]))
                else:
                    self.cells[row, col].set_text('')

    def error_dialog(self, message):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, message)
        dialog.run()
        dialog.destroy()

class SudokuEntry(Gtk.Entry):
    def __init__(self, row, col):
        Gtk.Entry.__init__(self)
        self.row = row
        self.col = col
        self.set_width_chars(1)
        self.set_max_length(1)
        self.props.margin = 2

win = SudokuWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
