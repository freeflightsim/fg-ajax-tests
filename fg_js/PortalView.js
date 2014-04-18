
Ext.define("FG.PortalView", {

extend: "Ext.tab.Panel",

requires: [
    "FG.PropsTreeBrowser",
    //"G2.samples.SamplesStore",
],


initComponent: function(){
    
    
    
    Ext.apply(this, {
        plain: true, bodyBorder: 0, border: 0,
        //disabled: true,
        items: [
            Ext.create("FG.Settings", {id: "settings"}),
            Ext.create("FG.PropsTreeBrowser", {id: "props_tree_browser"}),
           // Ext.create("G2.jobs.JobItemsGrid", {id: "job_items_grid"}),
           // Ext.create("G2.schedule.SchedulePanel", {id: "schedule_panel"})
        ],
        activeTab: 1
        
    });
    this.callParent();
    
    this.on("tabchange", function(panel, newCard, oldCard, eOpts){
        //newCard.show_help(false);
    }, this);
},

run_show: function(batch_id){
    //this.batch_id = batch_id;
    //this.setDisabled(false);
   /// this.load_data(DATA);
    return;
    Ext.Msg.wait("Loading...");
    Ext.Ajax.request({
        url: "/ajax/" + this.batch_id + "/schedule",
        method: "GET",
        scope: this,
        success: function( result ){
            
            var data = Ext.decode( result.responseText );
            //console.log("data", data);
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
    
},
load_data: function(data){
    return
    Ext.getStore("sample_types").loadData(data.sample_types);
    Ext.getStore("samples").loadData(data.samples); 
    
    Ext.getStore("test_cats").load_data(data);
    Ext.getStore("standards").loadData(data.standards);
    
    
    this.down("#job_panel").load_data(data);
    
    this.down("#samples_grid").load_data(data);
    this.down("#samples_grid").batch_id = this.batch_id;
    
    this.down("#job_items_grid").load_data(data);
    this.down("#job_items_grid").batch_id = this.batch_id;
    
    this.down("#schedule_grid").load_data(data);    
}


});
