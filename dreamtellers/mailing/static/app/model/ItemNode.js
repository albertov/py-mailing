Ext.define('WebMailing.model.ItemNode', {
    extend: 'WebMailing.model.Item',
    requires: [
        'WebMailing.model.Item'
    ],
    fields: ["record"],
    proxy: {type:'memory'},

    setRecord: function(record) {
        this.beginEdit();
        this.set('record', record);
        this.set('title', record.get('title'));
        this.set('modified', record.get('modified'));
        this.set('created', record.get('created'));
        this.endEdit();
    },

    isItem: function() {
        var nodeId = this.get('id');
        return nodeId && nodeId.indexOf('item-')>-1;
     },
    isCategory: function() {
        var nodeId = this.get('id');
        return nodeId && nodeId.indexOf('category-')>-1;
     },
     getRecordId: function() {
        var nodeId = this.get('id');
        return parseInt(nodeId.slice(nodeId.indexOf('-')+1), 0);
     }
        
});
