Ext.define('WebMailing.controller.Templates', {
    extend: 'Ext.app.Controller',
    views: ['template.Panel'],
    models: ['Template'],
    stores: ['Templates'],

    refs: [
        {
            selector: "templates",
            ref: "panel"
        }, {
            selector: "templates form",
            ref: "form"
        }
    ],

    init: function() {
        this.control({
            "templates": {
                render: this.onPanelRender
            },
            "templates template_grid": {
                select: this.onTemplateSelect,
                deselect: this.onTemplateDeSelect,
                beforedeselect: this.onBeforeDeselect,
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
    onBeforeDeselect: function(sm, record) {
        var f = this.getForm().getForm();
        if (f.getRecord() && f.isDirty()) {
            Ext.MessageBox.show({
                title: "Aviso", // i18n
                msg: "La plantilla contiene cambios sin guardar. ¿Desea guardarlos?",
                icon: Ext.MessageBox.WARNING,
                buttons: Ext.Msg.YESNOCANCEL,
                fn: function(btn) {
                    if (btn=="yes") {
                        f.updateRecord();
                    } else if (btn=="no") {
                        f.reset();
                    }
                }
            });
            return false;
        } else {
            return true;
        }
    },
    onTemplateDeSelect: function() {
        this.getPanel().setRecord(null);
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
