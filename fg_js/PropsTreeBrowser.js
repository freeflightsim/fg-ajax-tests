
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
            {text: "Init Load", handler: this.on_init_load ,scope: this}
            
        ],
        
        title: "Props Tree",
    store: store,
    rootVisible: false,
    });
    this.callParent();
    

},

on_init_load: function(){
    
    var feed_url = Ext.getCmp("settings_form").feed_url()
    
    //var SERVER = "http://localhost:9999/json/";
    Ext.data.JsonP.request({
        url: SERVER,
        params: {
            d: 5
        },
        callback: function (result) {
            console.log(result);
            if (response.success === true) {
                Ext.Msg.alert('Link Shortened', response.result, Ext.emptyFn);
            } else {
                Ext.Msg.alert('Error', response.result, Ext.emptyFn);
            }
        }
    });
    return
    
    Ext.Msg.wait("Loading...");
   
    Ext.Ajax.request({
        url: SERVER + "/json/",
        method: "GET",
        scope: this,
        success: function( result ){
            
            var data = Ext.decode( result.responseText );
            console.log("data", data);
            this.load_data(data);

            
            //= Set Titles
            //this.down("#job_items_grid").setTitle("Tests - <small>" + Ext.getStore("job_items").getCount() + "</small>");
            //this.down("#samples_grid").setTitle("Samples - <small>" + Ext.getStore("samples").getCount() + "</small>");
            
            this.setDisabled(false);
            Ext.Msg.hide();
        },
        failure: function(){
            this.my_unmask();
            G2.msg('Fail');
        }
    });
    
}

});