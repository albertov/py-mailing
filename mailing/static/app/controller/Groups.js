Ext.define('Mailing.controller.Groups', {
    extend: 'Ext.app.Controller',
    views: ['group.Panel'],
    models: ['Group'],
    stores: ['Groups'],

    init: function() {
        this.control({
            "groups": {
                render: this.onPanelRender,
            },
            "groups > group_grid": {
                new_item: this.onNewGroup,
                delete_item: this.onDeleteGroup
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Groups');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    },
    onNewGroup: function(grid) {
        var r = grid.store.add({
            name: 'Nombre' //i18n
        })[0];
        grid.rowEditor.startEdit(r, 0);
    },

    onDeleteGroup: function(grid, record) {
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
