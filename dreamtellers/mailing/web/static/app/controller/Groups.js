Ext.define('WebMailing.controller.Groups', {
    extend: 'Ext.app.Controller',
    views: ['group.Panel'],

    init: function() {
        this.control({
            "groups": {
                render: this.onPanelRender,
            },
            "group_grid": {
                new_item: this.onNewGroup,
                delete_item: this.onDeleteGroup,
                save_items: this.onSaveGroups
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
        record.store.remove(record);
    },

    onSaveGroups: function(grid) {
        grid.store.sync();
    }
});
