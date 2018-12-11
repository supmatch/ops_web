function enableSubmit(bool) {
        if(bool)$("#submit").removeAttr("disabled");
        else $("#submit").attr("disabled","disabled");
    }
    //需要验证多少行，就写多少个false
    var flags = [false,false,false,false,false,false];
    function v_submitbutton() {
        for(f in flags) if(!flags[f]){
            enableSubmit(false);
            return;
        }
        enableSubmit(true);
    }

    function lineState(name,msg){
	    $("."+name).text(msg);
    }
    //项目名
    function v_app_name() {
        var app_name = $("#app_name").val();
        if(app_name=="") {
            flags[0]=false;enableSubmit(false);
            lineState("app_name","*必填项");
        }
        else {flags[0]=true;lineState("app_name","");}
        v_submitbutton();
    }
    function check_name() {
        var app_name = $("#app_name").val();
        $.ajax({
            url:"/appmanager/CheckAppName/",
            type:"get",
            data:{app_name:app_name},
            success:function (data){
                if(data=='false'){
                    flags[0]=false;enableSubmit(false);
                    lineState("app_name","*项目已申请或已添加，请再次确认");
                }
                else {flags[0]=true;lineState("app_name","");}
                v_submitbutton();
            }
    });
    }
    //端口
    function v_app_port() {
        var app_port = $("#app_port").val();
        if(app_port==""){
            flags[1]=false;enableSubmit(false);
            lineState("app_port","*必填项");
        }
        else {flags[1]=true;lineState("app_port","");}
        v_submitbutton();
    }
    function check_port() {
        var app_port = $("#app_port").val();
        $.ajax({
            url:"/appmanager/CheckAppPort/",
            type:"get",
            data:{app_port:app_port},
            success:function (data){
                if(data=='false'){
                    flags[0]=false;enableSubmit(false);
                    lineState("app_port","*端口已被占用，请查看wiki确认");
                }
                else {flags[0]=true;lineState("app_port","");}
                v_submitbutton();
            }
    });
    }
    //dev环境ip
       function v_app_ip_dev() {
        var app_ip_dev = $("#app_ip_dev").val();
        if(app_ip_dev=="") {
            flags[2]=false;enableSubmit(false);
            lineState("app_ip_dev","*必填项");
        }
        else {flags[2]=true;lineState("app_ip_dev","");}
        v_submitbutton();
    }
    //test环境ip
       function v_app_ip_test() {
        var app_ip_test = $("#app_ip_test").val();
        if(app_ip_test=="") {
            flags[3]=false;enableSubmit(false);
            lineState("app_ip_test","*必填项");
        }
        else {flags[3]=true;lineState("app_ip_test","");}
        v_submitbutton();
    }
    //demo环境ip
       function v_app_ip_demo() {
        var app_ip_demo = $("#app_ip_demo").val();
        if(app_ip_demo=="") {
            flags[4]=false;enableSubmit(false);
            lineState("app_ip_demo","*必填项");
        }
        else {flags[4]=true;lineState("app_ip_demo","");}
        v_submitbutton();
    }
    //项目git地址
           function v_git_url() {
        var git_url = $("#git_url").val();
        if(git_url=="") {
            flags[5]=false;enableSubmit(false);
            lineState("git_url","*必填项");
        }
        else {flags[5]=true;lineState("git_url","");}
        v_submitbutton();
    }

    function adaptValue() {
        return true;
    }
