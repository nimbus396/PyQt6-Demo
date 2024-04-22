# PyQt6-Demo
<p>Regular forms with QT are fairly easy. Tables are not. To customize and sort, it took me a while to learn how to do different things. Hopefully, this demo will help someone out. The only requirments are PyQt6 and Pandas (only because I am lazy.)  
  
This demo sub-classes all the components normally used by a QTableView including the table view. These are the sub-classes.  

**QTableView** - Sub classed to add the context menu.  

**QViewHeader** - There weren't any good documents on painting cell headers under Windows so, I decided to buy the book "Create GUI Applications with Python & Qt6" by Martin Fitzpatrick. From that, I found out why I couldn't use BackgroundRole on headers and gave me the idea for painting my own header.  

**QAbstractItemModel** - This is used for the header model.  This includeds a mix of overridden and custom functions.

**QAbstractTableModel** - This is used for the data model and is accessed through the QSortFilterProxyModel() for filtering with a QComboBox. Includes a mix of overridden and custom functions. 

I also learned the complexities of list comprehension. At first, I had used a static list for the data but, I took a course on list comprehension and thought,
'why not?'. So, I created the two dimensional array of random length using list comprehension. Everytime it is run, the data changes.  

Along with sub-classing, this demo shows how to do different stylings for header and table. Personally, I would just use the default out of the box but, since this was a demo, I decided to go all in and figure out how to paint the app in different ways. The most frustrating part was figuring out how to paint a header cell. Everything else is fairly easy but, the way QT is compiled for Windows, it makes it very difficult to change header colors. I searched for many hours and then just dove in after watching some videos in C++".  

I am very happy with Qt at this point. I really enjoy Python and I am studying to be a Pythonista. A GUI engine is a great addition to Python. Although there are many out there, I am not sure why I settled on QT. I used WxWidgets for C++ many years ago but, for some reason, I got it stuck in my head to use Qt. WxWidgets (wxPython) is a great framework as well. Just pick one.... ( I am thinking of diving into it next and then do a comparison blog or something. )

As always, if there is a better way to do something in this demo, let me know. Coding is an art and though I have over 30 years of it, I am always .... always .... willing to learn something.</p>


In addition, there is a PyQT6 Simple Game screen demo.
