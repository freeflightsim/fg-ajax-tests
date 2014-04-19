
Ext.define("FG.PropsTreeBrowser", {

extend: "Ext.tree.Panel",

requires: [
    //"G2.samples.SampleTypesStore",
    //"G2.samples.SamplesStore",
],


initComponent: function(){
    
    var store = Ext.create('Ext.data.TreeStore', {
        root: {
            expanded: true,
            children: [
                { text: "detention", leaf: true },
                { text: "homework", expanded: true, children: [
                    { text: "book report", leaf: true },
                    { text: "algebra", leaf: true}
                ] },
                { text: "buy lottery tickets", leaf: true }
            ]
        }
    });
    
    Ext.apply(this, {
        plain: true, bodyBorder: 0, border: 0,
        tbar: [
            "->",
            {text: "Init Load", iconCls: "icoRefresh", handler: this.on_init_load ,scope: this}
            
        ],
        
        title: "Props Tree",
    store: store,
    rootVisible: false,
    });
    this.callParent();
    

},

on_init_load: function(){
    
    //Ext.Msg.wait("Loading...");   
    var frm = Ext.getCmp("settings_form"); // the form

    if( frm.is_ajax() ){
        
        //= Make and Ajax request
        Ext.Ajax.request({
            url: frm.fg_url(),
            method: "GET",
            scope: this,
            success: function( result ){
                
                var data = Ext.decode( result.responseText );
                console.log("data", data);
                this.load_data(data);
                this.setDisabled(false);
                Ext.Msg.hide();
            },
            failure: function(){
                ///this.my_unmask();
                //G2.msg('Fail');
                console.log("fail");
            }
        });
        
    } else {
        
        //= Fallback on JsonP request
        Ext.data.JsonP.request({
            url: frm.fg_url(),
            params: {
                d: 1
            },
            callbackKey: "callback",
            callback: function (result) {
                console.log(result);
                //if (response.success === true) {
                //    Ext.Msg.alert('Link Shortened', response.result, Ext.emptyFn);
                //} else {
                //    Ext.Msg.alert('Error', response.result, Ext.emptyFn);
                //}
            }
        });
        
    }
}

});