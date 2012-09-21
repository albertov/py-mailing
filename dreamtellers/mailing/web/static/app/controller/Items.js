Ext.define('WebMailing.controller.Items', {
    extend: 'Ext.app.Controller',
    views: ['item.Tree'],
    init: function(record, view) {
        this.record = record;
        view.setRecord(record);
        this.control({
            "item_tree": {
                'select': this.onRowSelect
            }
        });
    },
    onRowSelect: function(_, record) {
        console.debug(record);
    }
});
