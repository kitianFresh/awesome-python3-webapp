# awesome-python3-webapp
a web blog by python3 following [liaoxuefeng](http://www.liaoxuefeng.com)

## 笔记

### ORM知识点
#### orm的来源问题
  1. object-relation mapping,对象和关系的映射，从名字就可以看出是一个对象和一个关系数据库的记录的映射;
  2. 以JAVA为例，记得一开始编写程序的时候，连接数据库就是使用jdbc，然后做数据库操作，查找数据，比如查一个Student的信息，完了之后又将这条查询结果新建一个Student对象供程序使用，自己不停的需要写SQL语句。当更换对象比如Teacher时，又得重新写SQL，新建Teacher实例，如果要写回数据库，又得拿到对象的属性放入SQL语句中。并且当数据库表发生变化时，修改数据库操作代码也很麻烦;一个类和数据库表格没有很好的分离;下面这个Java代码:
```java
public User[] getUserInfoById(String id){
	try{
			String userid = (String)getProperty("login");
			if(userid == null){
				return null;
			}
			execSQL("select * from user where uid like ?","%"+id+"%");
			List<User> userlist = new ArrayList<User>();
			while(rs.next()){
				User user = new User();
				user.setUid(rs.getString("uid"));
				user.setPassword(rs.getString("password"));
				userlist.add(user);
																																		}
			User[] users = new User[userlist.size()];
			return userlist.toArray(users);
		}catch(Exception e){
			return null;
		}
}
```

  3. 如果用面向对象的思维就是，一个对象对数据库的增删该查可以直接作为这个对象的行为属性，而这个类还可以提供save，delete，update，find等数据库操作函数，并且程序员不用自己写过多SQL语句,直接传入相应的参数和条件即可。要想这个底层框架具有通用性，就必须可以在不知道类有哪些属性的情况下也可以使用，因为数据库和业务只有上层程序员知道，而这个框架本身不能知道有哪些字段和属性，必须自己扫描所有的字段和属性，然后形成映射关系，重新构造出一个新的类。当数据库表格发生变化(比如需求变更，增加一个字段),只需要修改对象定义，而不需要修改其他任何代码，代码也很容易维护。这里就涉及动态创造一个类的技术，Python使用了元类，Java中应该要使用反射机制来做ORM框架。
  4. 其实关系型数据库中实体entity的概念，直接对应的是OOP中类的概念，一个关系又对应了类和类之间的关系，一张表的一条记录对应了一个类实例即对象，对象对数据库的操作能抽象成相同的增删改查，底层封装SQL，上层提供一个和对象一样操作的接口即可。
  5. 目前对ORM的理解暂时到这里，后续希望能用java的reflection实现一个简单ORM。再做详细讨论;
#### python 中元类来动态生成一个类
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

### 后端markdown语法解析模块python-markdown2 以及相应的代码块渲染风格模块pygments pygments-css
  1. 采用markdown语法编辑博客，存入数据库的时纯markdown文本内容;
  2. 展示博客的时候需要将markdown文本转换成html，这里采用的是在后端用[python-markdown2](https://github.com/trentm/python-markdown2)进行转换，然后返回给前端;
  3. [pygments](http://pygments.org/),python3需要手动安装, [pygments-css](https://github.com/richleland/pygments-css)用来实现代码块语法高亮;

### 前端markdown语法解析模块marked.js和前端代码渲染模块highlight.js
  1. 增加了前端markdown语法解析器marked.js,他可以被vue.js当做过滤器来使用;
  2. 这里主要是当我编辑一篇博客的时候，希望可以在前端manage\_blog\_edit.html有WYSIWYG所见即所得的markdown编辑器;
  3. 在后端，我使用的是python-markdown2来转换markdown文本为html并返回给前端;
  4. 所以本博客混合使用了前端markdown和后端markdown，其实可以统一放到前端或者后端处理markdown语法，但是个人觉得统一放到前端更合适;
  5. 我在使用highlight.js检测pre code标签的时候使用了setInterval，原因是如果在一开始就直接调用一次hljs.highlightBlock(block);将无法渲染代码块，因为这个时候blog.html的代码块部分可能还没有加载过来，所以暂时只能间断性的轮询检测;
  6. 对于manage\_blog\_edit.html就必须使用setInterval轮询检测pre code标签了，因为在编写博客时，无法知道什么时候markdown中出现代码部分，除非修改marked.js,当用户输入代码时，触发hljs.highlightBlock(block)的调用;
