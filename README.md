# awesome-python3-webapp
a web blog by python3 following [liaoxuefeng](http://www.liaoxuefeng.com)

## 笔记

### ORM知识点
  1. 这里的Model实际上是一个词典，用于存储用户实例化的对象键值对，也就是每一个字段的实际值；
  2. 同时，他还存储了字段名字和数据库域的映射关系在\_\_mappings\_\_中，比如name---name，前者是string，后者是StringField类型，后者具有数据库列的属性，比如名字，类型，默认值，是否主键。

### Web知识点

### 前端vue.js和uikit知识点
  1. 分页的逻辑(类比OS进程虚拟地址空间分页);
   - 对于前端用户，第一需要展示当前页码page\_no和页大小(每页所含条目数)page\_size;第二需要展示是否有下一页has\_next以及是否有上一页has\_previous;第三展示每页不能重复，也就是说需要按照某种顺序展示;
   - 对于后端，用户请求的就是page\_no(当然更加复杂的用户可以更改page\_size和展示顺序orderBy),而数据在MySQL数据库中就是一张表，并且还有索引，如果直接查询，查询结果顺序就是无法预测的，所以必须先得到一个顺序固定的表，然后再将表分割成一页一页的逻辑，这里的计算逻辑和***操作系统分页***非常类似，这里需要的SQL技巧就是**orderBy**(使得顺序固定)和**limit**(查询某一个范围);
   - 最后，***为了方便前后端数据交换，直接实现一个Page对象***;他包括item\_count(总条目数) page\_size(页大小) page\_count(总页数) page\_index(当前页码) offset(页偏移) limit(页闭合区间) has\_next(是否有下一页) has\_previous(是否有前一页);通过Page对象实现前端展示逻辑和后端数据获取;

  2. 为了比较不同的分页方法，三种方法实现的分页展示;
   - 在manage\_blogs.html中并未使用自定义的组件v-pagination，而是***直接写了个和vm同级的元素；这样就不必进行父子组件的通讯任务了；但是会编写重复的代码***;
   - 在manage\_comments.html中使用***自定义组件v-pagination***，采用props和events dispatch[实现父子组件的通讯问题](http://vuejs.org/guide/components.html#Custom_Events);
     - ***vue.js 中的模板不能直接调用global functions***，所以直接调用gotoPage是不可行的(会出现scope.gotoPage undefined error);templates只能调用本作用域scope内的函数；
	 - 这里我改写了global gotoPage，以前是直接重新请求url得到新的页面(location.assign())，但是分页过程中只是改变了数据，并不改变视图，为了充分利用mvvm，所以我***采用getJson直接获取数据后自动引发view的更改***,而不是请求新的页面;
	 - 由于组件需要获得父组件的page数据，因此需要props和v-bind完成；另外，子组件需要更改父组件的数据page和comments，但是vue.js规定子组件最好不要直接更改父组件的数据;因此，选择使用event dispatch来做;
   - 在blogs.html页面中使用的是***服务端jinjia2模板的宏渲染***实现的分页,但这也是每次需要请求***新的页面***(因为渲染在后端进行，即对每一页的请求实际上是由服务端获取数据后并渲染完成最后的页面，直接展示给用户)而***不是新的数据***（即由前端vue.js来完成渲染视图更新）;

  3. mvvm中的模板类似于前端渲染，***mvvm数据驱动***;而jinjia2是后端模板渲染,计算主要由服务端进行;

### python-markdown2 pygments pygments-css
  1. 采用markdown语法编辑博客，存入数据库的时纯markdown文本内容;
  2. 展示博客的时候需要将markdown文本转换成html，这里采用的是在后端用[python-markdown2](https://github.com/trentm/python-markdown2)进行转换，然后返回给前端;
  3. [pygments](http://pygments.org/),python3需要手动安装, [pygments-css](https://github.com/richleland/pygments-css)用来实现代码块语法高亮;
