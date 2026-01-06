from config.apps.users.permissions.roles import Roles

ROLE_PERMISSIONS = {

    Roles.ADMIN.value: {
        "users:create",
        "users:read",
        "users:update",
        "users:delete",

        "store:create",
        "store:read",
        "store:update",

        "customer:create",
        "customer:read",
        "customer:update",
        "customer:delete",

        "supplier:create",
        "supplier:read",
        "supplier:update",
        "supplier:delete",

        "movements:create",
        "movements:read",
        "movements:update",

        "category:create",
        "category:read",
        "category:update",

        "subcategory:create",
        "subcategory:read",
        "subcategory:update",

        "items:create",
        "items:read",
        "items:update",
        "items:delete",

        "vehicle:create",
        "vehicle:read",
        "vehicle:update",
        "vehicle:delete",

        "facility:create",
        "facility:read",
        "facility:update",
        "facility:delete",
    },

    Roles.TECNICO.value: {
        "facility:create",
        "facility:read",
        "facility:update",

        "movements:create",
        "movements:read",

        "store:read",

        "customer:create",
        "customer:read",
        "customer:update",

        "items:create",
        "items:read",
        "items:update",

        "vehicle:read",
    },

    Roles.ADMINISTRATIVO.value: {
        "users:read",

        "store:read",

        "customer:create",
        "customer:read",
        "customer:update",

        "supplier:create",
        "supplier:read",
        "supplier:update",

        "items:create",
        "items:read",
        "items:update",

        "category:read",
        "subcategory:read",

        "movements:read",

        "facility:read",
    },
}
