from orator.migrations import Migration


class CreateBotUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('bot_users') as table:
            table.increments('id')
            table.big_integer('telegram_user_id')
            table.integer('driver_id').unsigned().nullable()
            table.foreign('driver_id').references('id').on('drivers')
            table.string('phone', 14).nullable()
            table.boolean('nal').default(False)
            table.boolean('brand').default(False)
            table.boolean('kids').default(False)
            table.boolean('booster').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('bot_users')
