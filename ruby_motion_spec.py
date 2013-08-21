import sublime
import sublime_plugin
import os
from subprocess import call

class RubyMotionSpecCommand(sublime_plugin.WindowCommand):
    def run(self):
        s = sublime.load_settings("RubyMotionSpec.sublime-settings")
        terminal = s.get("terminal")

        if terminal == 'iTerm':
            self.iterm_command()
        elif terminal == 'Terminal':
            self.terminal_command()
        else:
            self.sublime_command()

    def current_spec(self):
        return self.current_file().split('/')[-1].split('.')[0]

    def current_file(self):
        return self.window.active_view().file_name()

    def current_dir(self):
        return os.path.split(os.path.abspath(self.current_file()))[0]

    def iterm_command(self):
        command = """
            tell application "iTerm"
              tell the first terminal
                tell the current session
                  write text "rake spec files=%s"
                end tell
              end tell
            end tell
            """ % (self.current_spec())
        call(['osascript', '-e', command])

    def terminal_command(self):
        command = """
            tell application "Terminal"
              activate
              set currentTab to do script "rake spec files=%s" in window 0
            end tell
            """ % (self.current_spec())
        call(['osascript', '-e', command])

    def sublime_command(self):
        stdout = self.current_dir() + '/_stdout_spec'
        stderr = self.current_dir() + '/_stderr_spec'

        rake_spec = """
            rake spec files=%s SIM_STDOUT_PATH=%s SIM_STDERR_PATH=%s
            """ % (self.current_spec(), stdout, stderr)
        show_spec = """
            cat %s && cat %s
            """ % (stderr, stdout)
        clean_spec = """
            rm %s %s
            """ % (stderr, stdout)

        command = rake_spec + show_spec + clean_spec
        working_dir = self.current_dir()
        self.window.run_command("exec", {
            "cmd": [command],
            "shell": True,
            "working_dir": working_dir
        })