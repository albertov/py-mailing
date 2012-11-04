Ext.define('WebMailing.controller.Categories', {
    extend: 'Ext.app.Controller',
    views: ['category.Panel'],
    refs: [
        {
            ref: 'panel',
            selector: 'categories'
        }
    ],

    init: function() {
        this.control({
            "categories": {
                render: this.onPanelRender
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Categories');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    }
});
