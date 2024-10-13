import os
import sys
import platform

from subprocess import call

def view_replay(browser: str, log: str):
    on_windows = "Windows" in platform.system()

    output_filename = log.replace(".hlt", ".htm")
    path_to_file    = os.path.join("visualizer", output_filename)

    if on_windows:
        path_to_file = os.path.join(os.getcwd(), path_to_file)
        if not browser.endswith(".exe"):
            browser += ".exe"


    if not os.path.exists(output_filename):

        # parse replay file
        with open(log, 'r') as f:
            replay_data = f.read()

        # parse template html
        with open(os.path.join("visualizer", "Visualizer.htm")) as f:
            html = f.read()

        html = html.replace("FILENAME", log)
        html = html.replace("REPLAY_DATA", replay_data)

        # dump replay html file
        with open(os.path.join("visualizer", output_filename), 'w') as f:
            f.write(html)
    
    if on_windows:

        # add quotes to browser executable name/path if it contains whitespace or parantheses
        for c in " \t()":
            if c in browser:
                browser = '"' + browser + '"'
                break
        
        path_to_file = "file://" + path_to_file
    
    start_vis_cmd = f"{browser} {path_to_file}"

    if on_windows:
        start_vis_cmd = "start /B " + start_vis_cmd
    else:
        start_vis_cmd += " &"

    with open(os.devnull, "w") as null:
        call(start_vis_cmd, shell=True, stderr=sys.stderr, stdout=null)

def main():
    view_replay(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
