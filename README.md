# awesome-python3-webapp
a web blog by python3 following [liaoxuefeng](http://www.liaoxuefeng.com)

## 笔记
---
### ORM知识点
  1. 这里的Model实际上是一个词典，用于存储用户实例化的对象键值对，也就是每一个字段的实际值；
  2. 同时，他还存储了字段名字和数据库域的映射关系在\_\_mappings\_\_中，比如name---name，前者是string，后者是StringField类型，后者具有数据库列的属性，比如名字，类型，默认值，是否主键。
---
### Web知识点

---
### 前端vue.js和uikit知识点
  1. 分页的逻辑(类比OS进程虚拟地址空间分页);
  2. 为了比较不同的分页方法，三种方法实现的分页;
   - 在manage\_blogs\.html中并未使用自定义的组件v-pagination，而是直接写了个和vm同级的元素；这样就不必进行父子组件的通讯任务了；但是会编写重复的代码;
   - 在manage\_comments\.html中使用自定义组件v-pagination，采用props和events dispatch[实现父子组件的通讯问题](http://vuejs.org/guide/components.html#Custom_Events);
    - vue.js 中的模板不能直接调用global functions，所以直接调用gotoPage是不可行的(会出现scope.gotoPage undefined error);templates只能调用本作用域scope内的函数；
	- 这里我改写了global gotoPage，以前是直接重新请求url得到新的页面，但是分页过程中只是改变了数据，并不改变视图，为了充分利用mvvm，所以我采用getJson直接获取数据后自动引发view的更改,而不是请求新的页面;
	- 由于组件需要获得父组件的page数据，因此需要props和v-bind完成；另外，子组件需要更改父组件的数据page和comments，但是vue.js规定子组件最好不要直接更改父组件的数据;因此，选择使用event dispatch来做;
  
  3. mvvm中的模板类似于前端渲染，而jinjia2是后端模板渲染;

