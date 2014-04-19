
Ext.define("FG.Settings", {

extend: "Ext.form.Panel",

requires: [
    //"G2.samples.SampleTypesStore",
    //"G2.samples.SamplesStore",
],


initComponent: function(){
    
    
    Ext.apply(this, {
        plain: false, frame: true, bodyBorder: 0, border: 0,
        //title: "Settings",
        padding: 10,
        margin:  10,
        defaults: {
           labelWidth: 60, labelAlign: "right",
        }, 
        items: [
            {name: "host", fieldLabel: "fg server",  xtype: "textfield", value: "localhost"},
            {name: "port", fieldLabel: "Port",  xtype: "numberfield", value: "9999"},
            {xtype: "fieldset", title: "Request Type",
                items: [
                    {xtype: "radio", name: "rtype", value: "ajax", boxLabel: "Ajax", myName: "ajax"},
                    {xtype: "radio", name: "rtype", value: "jsonp", boxLabel: "JsonP", checked: true},
                ]
            },
            
        ]
        
    });
    this.callParent();
},

fg_url: function(){
    // is there a neater way than this ?
    return "http://" + this.down("[name=host]").getValue() + ":" + this.down("[name=port]").getValue() + "/json/";
},
is_ajax: function(){
    return this.down("[myName=ajax]").getValue() === true;
}

});