#! /usr/bin/env python
# todiscgui_ex.py

"""Experimental todisc GUI using only meta.py widgets.

//Note: This isn't fully implemented yet--I'm writing the docs first.//

This module demonstrates a simplified approach to creating GUIs for
command-line programs. It's designed so _anyone_ can easily write their
own GUI, without having any programming experience.

It assumes your GUI is a direct frontend to a command-line program, with
each command-line option having an associated GUI control widget. Say, if
your program takes input and output filenames:

    $ tovid -in movie.avi -out movie_encoded

then you can create GUI widgets for those options like this:

    ('in', Filename, "Input filename")
    ('out', Filename, "Output prefix")

Command-line options are associated with GUI widgets by enclosing a tuple of
things in parentheses. These have the general format:

    ('option', Metawidget, "Label", ...)

where 'option' is a command-line option (without the leading '-'), Metawidget
is a class like Filename, Choice, or Number, describing what type of value the
option sets, and "Label" is the text that should appear next to the GUI widget
that controls the option's value. Other parameters describe the option,
its default value, and hints about how to draw the GUI control widget; they
are specific to the flavor of Metawidget being used.

Related options are grouped in a Panel by providing a panel name, and a
comma-separated list of option tuples:

    general = Panel("General",
        ('bgaudio', Filename, "Background audio file"),
        ('submenus', Flag, "Create submenus"),
        ('menu-length', Number, "Length of menu (seconds)", 0, 120)
        )

This will create three GUI widgets in a panel labeled "General": one for typing
or browsing to a filename, one for enabling or disabling submenus, and another 
for setting menu length to a number between 0 and 120.

To create the GUI with only this one panel, you can do this:

    app = Application("todisc GUI", 'todisc', general)
    app.run()

This creates the GUI, draws all the widgets, and will run your command-line
program at the push of a button.

If your program has a lot of options, one panel may not be enough to hold them
all without looking cluttered, so you may break them down into multiple Panels,
which will be shown in the GUI as tabs that you can switch between. Create a
list of Panels like this:

    panels = [
        Panel("Thumbnails",
            ('thumb-mist-color', Color, ...),
            ('wave', Text, ...)
        ),
        Panel("Text and Font",
            ('menu-font', Font, ...),
            ('menu-fontsize', Number, ...)
        )
    ]

Once you have a panel or list of panels, you can create the GUI and run it
like this:

    app = Application("todisc GUI", 'todisc', panels)
    app.run()


"""

# Get all the Metawidgets we'll need
from libtovid.gui.meta import *

# Panels, grouping together related options
main = Panel("Main",
    ('files', FileList, 'required',
        'Input video files'),
    ('titles', TextList, 'required',
        'Video titles')
    )

# (option, Metawidget, label, default, ...) or
# (option, Metawidget, 'required', label, default, ...)
general = Panel("General",
    ('showcase', Filename, 'required',
        'Showcase', '',
        'Image or video file to be showcased in a large central frame',
        'load', 'Select an image or video file.'),
    ('background', Filename, 'required',
        'Background', '',
        'Image or video displayed in the background of the main menu',
        'load', 'Select an image or video file'),
    ('bgaudio', Filename, 'required',
        'Audio', '',
        'Audio file played while the main menu is showing',
        'load', 'Select an audio file'),
    ('submenus', Flag,
        'Create submenus', False),
    ('static', Flag,
        'Static menus (takes less time)', False),
    ('menu-title', Text,
        'Menu title', '',
        'Title of the main menu'),
    ('menu-length', Number,
        'Menu length', 30,
        'Duration of menu in seconds',
        0, 120, 'scale'),
    ('keep-files', Flag,
        'Keep useful intermediate files on exit', False),
    ('no-ask', Flag,
        'No prompts for questions', False),
    ('no-warn', Flag,
        'Do not pause at warnings', False),
    ('use-makemenu', Flag,
        'Use makemenu', False,
        'Create menus using the makemenu script instead of todisc'),
    ('tovidopts', Text,
        'Custom tovid options', '',
        "Space-separated list of options to pass to tovid for encoding.")
)

menu = Panel("Menu",
    ('ani-submenus', Flag,
        'Animated submenus (takes more time)', False,
        'tooltip'),
    ('menu-fade', Flag,
        'Fade in menu', False,
        'tooltip'),
    ('seek', List,
        'Seek time', '',
        'Play thumbnail videos from the given seek time (seconds)'),
    ('bgvideo-seek', Number,
        'Background video seek time', 2,
        'Play background video from the given seek time (seconds)',
        0, 3600, 'scale'),
    ('bgaudio-seek', Number,
        'Background audio seek time', 2,
        'Play background audio from the given seek time (seconds)',
        0, 3600, 'scale'),
    ('showcase-seek', Number,
        'Showcase video seek time', 2,
        'Play showcase video from the given seek time (seconds)',
        0, 3600, 'scale'),
    ('align', Choice,
        'Montage alignment', 'north',
        'Controls positioning of the thumbnails and their titles',
        'north|south|east|west'),
    ('intro', Filename,
        'Intro video', '',
        'Video to play before showing the main menu',
        'load', 'Select a video file'),
    ('showcase-titles-align', Choice,
        'Video(s) title alignment', 'west',
        'tooltip',
        'west|east|center'),
    ('showcase-framestyle', Choice,
        'Showcase frame style', 'none',
        'tooltip',
        'none|glass'),
    ('showcase-geo', Text,
        'Showcase image position (XxY', '',
        'tooltip')
)

# Throw in a few 'required' options just for fun
thumbnails = Panel("Thumbnails",
    ('3dthumbs', Flag,
        'Create 3D thumbs', False,
        'tooltip'),
    ('thumb-shape', Choice, 'required',
        'Thumb shape', 'normal',
        'tooltip',
        'normal|oval|plectrum|egg'),
    ('opacity', Number, 'required',
        'Thumbnail opacity', 100,
        'tooltip',
        1, 100, 'spin'),
    ('blur', Number, 'required',
        'Blur', 4,
        'tooltip',
        1, 5, 'spin'),
    ('rotate-thumbs', List, 'required',
        'Rotate Thumbs (list)', '',
        'tooltip'),
    ('wave', Text, 'required',
        'Wave effect for showcase thumb', 'default',
        'tooltip'),
    ('rotate', Number, 'required',
        'Rotate Showcase thumb', 5,
        'tooltip',
        -30, 30, 'spin'),
    ('thumb-mist-color', Color, 'required',
        'Thumb mist color', 'white',
        'tooltip'),
    ('tile3x1', Flag,
        'Arrange thumb montage in 1 row of 3 thumbs', False,
        'tooltip')
)


audio = Panel("Audio",
    ('menu-audio-length', Number,
        'Menu audio length', 30,
        'tooltip',
        0, 120, 'scale'),
    ('menu-audio-fade', Number,
        'Menu audio fade', 1,
        'tooltip',
        0, 10, 'scale'),
    ('submenu-audio', Filename,
        'Submenu audio file', '',
        'tooltip',
        'load', 'Select an audio file, or video file with audio'),
    ('submenu-audio-length', Number,
        'Submenu audio length', 30,
        'tooltip',
        0, 120, 'scale'),
    ('submenu-audio-fade', Number,
        'Submenu audio fade', 1,
        'tooltip',
        0, 10, 'scale')
)


text = Panel("Text and Font",
    ('menu-font', Font,
        'Menu title font', 'Helvetica',
        'tooltip'),
    ('thumb-font', Font,
        'Video title(s) font', 'Helvetica',
        'tooltip'),
    ('menu-fontsize', Number,
        'Menu title font size', 20,
        'tooltip',
        0, 80, 'scale'),
    ('thumb-fontsize', Number,
        'Video title(s) font size', 12,
        'tooltip',
        0, 80, 'scale'),
    ('title-color', Color,
        'Title color', '',
        'tooltip'),
    ('submenu-title-color', Color,
        'Submenu title color', '',
        'tooltip'),
    ('thumb-text-color', Color,
        'Video title(s) color', '',
        'tooltip'),
    ('text-mist', Flag,
        'Text mist', False,
        'tooltip'),
    ('text-mist-color', Color,
        'Text mist color', '',
        'tooltip'),
    ('text-mist-opacity', Number,
        'Text mist opacity', 60,
        'tooltip',
        1, 100, 'spin'),
    ('menu-title-geo', Choice,
        'Menu title position', 'south',
        'tooltip',
        'north|south|west|east|center'),
    ('menu-title-offset', Text,
        'Offset for menu title position', '+0+0',
        'tooltip'),
    ('stroke-color', Color,
        'Stroke color', '',
        'tooltip'),
    ('submenu-stroke-color', Color,
        'Submenu stroke color', '',
        'tooltip'),
    ('title-gap', Number,
        'Space between Textmenu titles (pixels)', 2,
        'tooltip',
        0, 400, 'spin'),
    ('text-start', Number,
        'Start Textmenu titles at: (pixels)', 2,
        'tooltip',
        0, 460, 'spin')
)

authoring = Panel("Authoring",
    ('chapters', List,
        'Number of Chapters', '',
        'Single value or list'),
    ('chain-videos', List,
        'Chain videos together', '',
        'See "man todisc" for details'),
    ('widescreen', Choice,
        'Widescreen', None,
        'tooltip',
        'nopanscan|noletterbox'),
    ('aspect', Choice,
        'Aspect ratio', '4:3',
        'tooltip',
        '4:3|16:9'),
    ('highlight-color', Color,
        'Highlight color', '',
        'tooltip'),
    ('select-color', Color,
        'Selection color', '',
        'tooltip'),
    ('button-style', Choice,
        'Button style', 'rect',
        'tooltip',
        'rect|text|text-rect'),
    ('audio-lang', List,
        'Default audio language', '',
        'Single value or list'),
    ('subtitles', List,
        'Default subtitle language', '',
        'Single value or list'),
    ('outlinewidth', Number,
        'Outlinewidth for spumux buttons', 4,
        'tooltip',
        0, 20, 'scale'),
    ('loop', Number,
        'Loop', 10,
        'tooltip',
        0, 30, 'scale'),
    ('playall', Flag,
        '"Play all" button', False,
        'tooltip')
)

# A list of all panels, shown in tabs in this order
panels = [
    #main,
    general,
    menu,
    thumbnails,
    audio,
    text,
    authoring
]

# Create and run the application
todiscgui = Application('todisc', 'todisc GUI', panels)
todiscgui.run()
