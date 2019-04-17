# tri
Generate a random low-poly style wallpaper based on the time of day.

## Use and Installation
`brain.py` can be run directly from the commandline or can be run systematically with `Windows Task Scheduler`

Use the following command in your terminal:
`schtasks /Create /SC HOURLY /TN triWallpaper /TR "<PATH_TO_PYTHONW_EXE> <PATH_TO_PYTHON_SCRIPT>"`
[Credit to Glen Robertson on stack overflow](https://stackoverflow.com/questions/2725754/schedule-python-script-windows-7)

**Use `pythonw.exe`** so that the task will run silently without openning a terminal window and gaining focus while you're doing other tasks

## Support
This project currently only supports Windows Operating Systems

## Dependencies

The following python libraries are required:
* `scipy`
* `skimage`
* `numpy`
* `colour` 
