
Ext.define("FG.Settings", {

extend: "Ext.form.Panel",

requires: [
    //"G2.samples.SampleTypesStore",
    //"G2.samples.SamplesStore",
],


initComponent: function(){
    
    
    Ext.apply(this, {
        plain: true, bodyBorder: 0, border: 0,
        title: "Settings",
        
    });
    this.callParent();
    

}

});