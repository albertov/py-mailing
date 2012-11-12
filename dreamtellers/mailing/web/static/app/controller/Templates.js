Ext.define('WebMailing.controller.Templates', {
    extend: 'Ext.app.Controller',
    views: ['template.Panel'],
    models: ['Template'],
    stores: ['Templates'],

    refs: [
        {
            selector: "templates",
            ref: "panel"
        }
    ],

    init: function() {
        this.control({
            "templates": {
                render: this.onPanelRender
            },
            "templates template_grid": {
                select: this.onTemplateSelect,
                new_item: this.onNewTemplate,
                delete_item: this.onDeleteTemplate
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Templates');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    },
    onTemplateSelect: function(grid, record) {
        this.getPanel().setRecord(record);
    },
    onNewTemplate: function(grid) {
        var r = grid.store.add({
            title: 'Título', //i18n
            type: 'xhtml'
        })[0];
        grid.store.on('write', function() {
            grid.rowEditor.startEdit(r, 0);
        }, this, {single:true})
    },


    onDeleteTemplate: function(grid, record) {
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.get('title')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    }
});
