Ext.define('Mailing.controller.Images', {
    extend: 'Ext.app.Controller',
    views: ['image.Panel', 'image.NewImageWindow', 'image.EditWindow'],
    models: ['Image'],
    stores: ['Images'],
    refs: [
        {
            ref: 'grid',
            selector: 'image_grid'
        }
    ],

    init: function() {
        this.control({
            "images": {
                render: this.onPanelRender,
            },
            "new_image_window": {
                "new": this.onNewImage,
            },
            "image_grid": {
                new_item: this.showNewImageWindow,
                delete_item: this.onDeleteImage,
                edit_item: this.onEditImage
            },
            "image_edit_window": {
                upload: this.onImageUpload,
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Images');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    },
    onNewImage: function(win) {
        var me=this, form = win.down('form').getForm();
        form.submit({
            url: url('image/upload'),
            waitMsg: 'Subiendo imágen al servidor...', //i18n
            timeout: 30,
            success: function(fp, o) {
                var s = Ext.getStore('Images'),
                    records = s.getProxy().getReader().read(o.result).records;
                s.add(records);
                me.getGrid().getSelectionModel().select(records);
                win.close();
            },
            failure: function(fp, o) {
                console.debug('failure', arguments);
                if (o.result && o.result.errors) {
                    fp.markInvalid(o.result.errors);
                } else {
                    Ext.MessageBox.show({
                        title: "Error del servidor", // i18n
                        msg: o.result?o.result.message:'',
                        icon: Ext.MessageBox.ERROR,
                        buttons: Ext.Msg.OK
                    });
                    win.close();
                }
            }
        });
    },

    showNewImageWindow: function() {
        var win = Ext.create('Mailing.view.image.NewImageWindow');
        win.show();
    },

    onEditImage: function(btn, record) {
        var win = Ext.widget('image_edit_window');
        win.down('form').loadRecord(record)
        win.show();
    },
    
    onImageUpload: function(win, form) {
        var record = form.getRecord();
        form.submit({
            url: url('image/'+record.get('id')),
            waitMsg: 'Subiendo imágen al servidor...', //i18n
            timeout: 30,
            success: function(fp, o) {
                var s = Ext.getStore('Images');
                s.reload();
                win.close();
            },
            failure: function(fp, o) {
                console.debug('failure', arguments);
                if (o.result && o.result.errors) {
                    fp.markInvalid(o.result.errors);
                } else {
                    Ext.MessageBox.show({
                        title: "Error del servidor", // i18n
                        msg: o.result?o.result.message:'',
                        icon: Ext.MessageBox.ERROR,
                        buttons: Ext.Msg.OK
                    });
                    win.close();
                }
            }
        });
    },

    onDeleteImage: function(grid, record) {
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.get('filename')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    }
});
