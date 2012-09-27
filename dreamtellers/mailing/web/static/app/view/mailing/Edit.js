Ext.define('WebMailing.view.mailing.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.mailing.Form',
        'WebMailing.view.item.Edit'
    ],
    alias: 'widget.mailing_edit',
    layout: 'border',
    border: false,
    items: [
        {
            xtype: 'mailing_form',
            region: 'north',
            height: 80,
            split: true
        }, {
            xtype: 'item_edit',
            region: 'center'
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.down('mailing_form').loadRecord(record);
        this.down('item_edit').setMailing(record);
    }
});
