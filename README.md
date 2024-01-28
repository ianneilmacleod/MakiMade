# Maki Made Workshop
Projects to support Maki Made maker workshop.

I retired from geoscience in 2018, and I now spend a lot of time in my workshop making things.  While I no longer work with 
geoscience data, my [Geosoft roots run deep](https://wiki.seg.org/wiki/Ian_MacLeod), 
particularly using the Geosoft approach to data processing.

Before retirement, I was very motivated to expose more of the Geosoft processing environment to Python. The intention was to allow 
Geosoft customers to more easily integrate the work they do with Geosoft environment and their own needs for geoscience data processing.
In particular, Geosoft exposed all data read and write API functions to open access (no license required), and together with
[Geosoft's freely-available viewer](https://www.seequent.com/products-solutions/geosoft-viewer/), this provides a remarkably useful
way to deal with geophysical and other spatial data formats.

In this project, I am using [Geosoft's GX developer](https://geosoftgxdev.atlassian.net/wiki/spaces/GD/pages/44367874/Python+in+GX+Developer)
to work with spatial data as I make things in my workshop, where I use 3D printers and 
CNC machines together with a full compliment of woodworking machines and tools.  For example, I want to make carved DEM models of places
of interest. To do this I need to download DEM data, reproject the data to a useful coordinate system, resample and de-alias the data to
scale, and save the DEM as a 3D STL.  I can then load the stl into either my 3D printer slicing application (IdeaMaker for my Raise 3D E2 
printer), or to Fusion360 to use modelling and CAM features that create Gcode for my CNC macine (Onefinity Elite Journeyman).

Chronology notes
----------------

(2024-01-28) After 6 years away from Geosoft, I am relearning Python and Geosoft. I will document my journey here.

## Reference

[GX Developer documentation](https://geosoftgxdev.atlassian.net/wiki/display/GD/Python+in+GX+Developer)

[GXAPI reference](https://geosoftinc.github.io/gxpy/9.5/python/geosoft.gxapi.classes.html)

[GXPY reference](https://geosoftinc.github.io/gxpy/9.5/python/geosoft.gxpy.html#gxpy)

[Geosoft GX Language reference](https://geosoftgxdev.atlassian.net/wiki/spaces/GXD93/pages/78020870/Geosoft+GX+Language)

[Geosoft Inc. on Github](https://github.com/GeosoftInc)
