Ext.define('Mailing.controller.Templates', {
    extend: 'Ext.app.Controller',
    views: ['template.Panel', 'template.UploadWindow'],
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
                beforedeselect: this.checkIfSaveIsNeeded,
                new_item: this.onNewTemplate,
                delete_item: this.onDeleteTemplate
            },
            "templates button[itemId=upload]": {
                click: this.onTemplateUpload
            },
            "templates button[itemId=download]": {
                click: this.onTemplateDownload
            }
        });
        this.templates = Ext.getStore('Templates');
        this.mon(this.templates, 'beforeload', this.checkIfSaveIsNeeded, this);
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
    checkIfSaveIsNeeded: function() {
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
        if (!this.checkIfSaveIsNeeded())
            return;
        var r = grid.store.add({
            title: 'Título', //i18n
            type: 'xhtml'
        })[0];
        grid.store.on('write', function() {
            grid.rowEditor.startEdit(r, 0);
        }, this, {single:true})
    },
    onTemplateUpload: function() {
        var record = this.getForm().getForm().getRecord(),
            win = Ext.widget('template_upload_window', {
                listeners: {
                    scope: this,
                    upload: this.onTemplateUploadSubmit
                }
            });
        win.down('form').loadRecord(record);
        win.show();
    },
    onTemplateUploadSubmit: function(win, form) {
        var record = this.getForm().getForm().getRecord();
        form.submit({
            url: url('template/'+record.get('id')),
            waitMsg: 'Subiendo plantilla al servidor...', //i18n
            timeout: 30,
            success: function(fp, o) {
                var template = o.result.templates[0];
                record.store.suspendAutoSync();
                record.set('body', template.body);
                record.set('type', template.type);
                record.commit();
                form.loadRecord(record);
                record.store.resumeAutoSync();
                win.close();
            },
            failure: function(fp, o) {
                Ext.MessageBox.show({
                    title: "Error del servidor", // i18n
                    msg: o.result?o.result.message:'',
                    icon: Ext.MessageBox.ERROR,
                    buttons: Ext.Msg.OK
                });
                win.close();
            }
        });
    },
    onTemplateDownload: function() {
        var record = this.getForm().getForm().getRecord();
        window.open(url('template/'+record.get('id')+'/body'));
    },
    onDeleteTemplate: function(grid, record) {
        if (!this.checkIfSaveIsNeeded())
            return;
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
