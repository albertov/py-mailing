Ext.define('Mailing.view.image.Combo', {
    extend: 'Mailing.ComboGrid',
    requires: [
        'Mailing.view.image.Grid',
        'Mailing.store.Images'
    ],
    alias: 'widget.image_combo',
    gridClass: 'Mailing.view.image.Grid',
    listConfig: {
        minWidth: 200,
        plugins: []
    },
    forceSelection: true,
    valueField: 'id',
    pageSize: 10,
    typeAhead: true,
    triggerAction: 'all',
    minChars: 1,
    matchFieldWidth: false,
    queryMode: 'local',
    queryField: 'title',
    displayField: 'filename',
    initComponent: function() {
        this.store = Ext.create('Mailing.store.Images', {
            pageSize: this.pageSize||100,
            buffered: false
        });
        this.callParent(arguments);
        this.on('beforequery', function() {
            this.store.clearFilter();
            delete this.lastQuery;
        }, this);
    },
    doQuery: function(queryString, forceAll, rawQuery) {
        if (forceAll) {
            this.clearValue();
        }
        var displayField = this.displayField, ret;
        this.displayField = this.queryField || this.displayField;
        try {
            ret = this.callParent(arguments);
        } catch(e) {
            this.displayField = displayField;
            throw (e);
        }
        this.displayField = displayField;
    },
    setValue: function(value) {
        // makes sure record is loaded in store
        if ( !this.store.loading &&
            (Ext.isNumber(value) || Ext.isString(value)) &&
            this.store.find(this.valueField, value)<0)
        {
            console.debug('setValue', value);
            this.store.load({
               filters: [{property: this.valueField, value:value}],
               page: 1,
               start: 0,
               limit: 1
            });
        }
        this.callParent(arguments);
    },
    assertValue: function() {
        // Allow blank selection
        if (this.getRawValue()) {
            this.callParent(arguments);
        }
    }
});
