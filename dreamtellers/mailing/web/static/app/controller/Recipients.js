Ext.define('WebMailing.controller.Recipients', {
    extend: 'Ext.app.Controller',
    views: ['recipient.Panel'],
    models: ['Recipient'],
    stores: ['Recipients'],

    init: function() {
        this.control({
            "recipients": {
                render: this.onPanelRender,
            },
            "recipient_grid": {
                new_item: this.onNewRecipient,
                delete_item: this.onDeleteRecipient
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
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.get('name')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    }
});
