Ext.define('WebMailing.controller.Recipients', {
    extend: 'Ext.app.Controller',
    views: ['recipient.Panel'],

    init: function() {
        this.control({
            "recipients": {
                render: this.onPanelRender,
            },
            "recipient_grid": {
                new_item: this.onNewRecipient,
                delete_item: this.onDeleteRecipient,
                save_items: this.onSaveRecipients
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Recipients');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    },
    onNewRecipient: function(grid) {
        var r = grid.store.add({
            name: 'Nombre', //i18n
            email: 'email@example.com' //i18n
        })[0];
        grid.rowEditor.startEdit(r, 0);
    },

    onDeleteRecipient: function(grid, record) {
        record.store.remove(record);
    },

    onSaveRecipients: function(grid) {
        grid.store.sync();
    }
});
