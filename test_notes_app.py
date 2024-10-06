import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk, Text
import os
import builtins
import notes_app


class TestTextEditorApp(unittest.TestCase):

    def setUp(self):
        """Create a test window and text area."""
        self.window = Tk()
        self.text_area = Text(self.window)

    def tearDown(self):
        """Destroy the test window after each test."""
        self.window.destroy()

    @patch('tkinter.filedialog.askopenfilename', return_value='test_file.txt')
    @patch('builtins.open', new_callable=MagicMock)
    def test_open_file(self, mock_open, mock_askopenfilename):
        """Test the open_file function."""
        mock_open.return_value.read.return_value = "Test content"

        notes_app.open_file()

        mock_open.assert_called_with('test_file.txt', 'r')
        self.assertEqual(self.text_area.get(1.0, 'end-1c'), "Test content")

    @patch('tkinter.filedialog.asksaveasfilename', return_value='test_save.txt')
    @patch('builtins.open', new_callable=MagicMock)
    def test_save_file(self, mock_open, mock_asksaveasfilename):
        """Test the save_file function."""
        self.text_area.insert(1.0, "Test save content")
        notes_app.save_file()

        mock_open.assert_called_with('test_save.txt', 'w')
        mock_open.return_value.write.assert_called_with("Test save content\n")

    def test_new_file(self):
        """Test the new_file function."""
        self.text_area.insert(1.0, "Old content")
        notes_app.new_file()

        self.assertEqual(self.text_area.get(1.0, 'end-1c'), "")

    @patch('tkinter.colorchooser.askcolor', return_value=('gray', '#808080'))
    def test_change_color(self, mock_askcolor):
        """Test changing text color."""
        notes_app.change_color()

        self.assertEqual(self.text_area.cget("fg"), '#808080')

    def test_change_font(self):
        """Test changing the font."""
        notes_app.font_name.set("Courier")
        notes_app.font_size.set(12)

        notes_app.change_font()

        self.assertEqual(self.text_area.cget("font"), ('Courier', 12))

    @patch('tkinter.messagebox.showinfo')
    def test_about(self, mock_showinfo):
        """Test the about dialog."""
        notes_app.about()

        mock_showinfo.assert_called_with("About this program", "This is a program written by yo mum")

    @patch('text_editor_app.window.quit')  # Mocking the quit method of the window
    def test_quit(self, mock_quit):
        """Test quitting the app."""
        notes_app.quit()

        mock_quit.assert_called()

    def test_cut(self):
        """Test the cut operation."""
        self.text_area.insert(1.0, "Test cut")
        self.text_area.tag_add("sel", "1.0", "1.4")
        notes_app.cut()

        self.assertEqual(self.text_area.get(1.0, 'end-1c'), " cut")

    def test_copy(self):
        """Test the copy operation."""
        self.text_area.insert(1.0, "Test copy")
        self.text_area.tag_add("sel", "1.0", "1.4")
        notes_app.copy()

        clipboard_content = self.window.clipboard_get()
        self.assertEqual(clipboard_content, "Test")

    def test_paste(self):
        """Test the paste operation."""
        self.window.clipboard_clear()
        self.window.clipboard_append("Paste content")

        notes_app.paste()

        self.assertEqual(self.text_area.get(1.0, 'end-1c'), "Paste content")


if __name__ == "__main__":
    unittest.main()