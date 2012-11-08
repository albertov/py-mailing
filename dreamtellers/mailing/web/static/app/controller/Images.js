Ext.define('WebMailing.controller.Images', {
    extend: 'Ext.app.Controller',
    views: ['image.Panel', 'image.NewImageWindow'],
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
                save_items: this.onSaveImages
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
            url: 'image/upload',
            waitMsg: 'Subiendo imágen al servidor...', //i18n
            timeout: 30,
            success: function(fp, o) {
                var image = o.result.images[0];
                var r = Ext.getStore('Images').add(image);
                me.getGrid().getSelectionModel().select(r);
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
        var win = Ext.create('WebMailing.view.image.NewImageWindow');
        win.show();
    },

    onDeleteImage: function(grid, record) {
        record.store.remove(record);
    },

    onSaveImages: function(grid) {
        grid.store.sync();
    }
});
