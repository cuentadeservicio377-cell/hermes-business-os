import { getCompanyConfig } from "@/lib/data";
import { Building2, Palette, Mail, Phone, MapPin } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function ConfiguracionPage() {
  const config = await getCompanyConfig();
  const empresa = config?.empresa || {};
  const departamentos = config?.departamentos || {};
  const integraciones = config?.integraciones || {};

  const deptLabels: Record<string, string> = {
    ventas: "Ventas",
    operaciones: "Operaciones",
    documentos: "Documentos",
    finanzas: "Finanzas",
    rrhh: "RRHH",
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Configuración</h1>
        <p className="text-gray-500 mt-1">Información de tu empresa</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Company Info */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-primary-50 rounded-lg">
              <Building2 size={20} className="text-primary-600" />
            </div>
            <h2 className="text-lg font-semibold">Información General</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Nombre de la empresa</label>
              <p className="text-lg font-semibold">{empresa.nombre || "No configurado"}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Industria</label>
                <p className="capitalize">{empresa.industria || "No configurado"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Tamaño</label>
                <p className="capitalize">{empresa.tamano || "No configurado"}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Moneda</label>
                <p>{empresa.moneda || "MXN"}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Idioma</label>
                <p className="uppercase">{empresa.idioma || "es"}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Contact */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-blue-50 rounded-lg">
              <Mail size={20} className="text-blue-600" />
            </div>
            <h2 className="text-lg font-semibold">Contacto</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Mail size={16} className="text-gray-400" />
              <div>
                <label className="text-sm font-medium text-gray-600">Email</label>
                <p>{empresa.contacto?.email || "No configurado"}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Phone size={16} className="text-gray-400" />
              <div>
                <label className="text-sm font-medium text-gray-600">Teléfono</label>
                <p>{empresa.contacto?.telefono || "No configurado"}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <MapPin size={16} className="text-gray-400" />
              <div>
                <label className="text-sm font-medium text-gray-600">Dirección</label>
                <p>{empresa.contacto?.direccion || "No configurado"}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Branding */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-purple-50 rounded-lg">
              <Palette size={20} className="text-purple-600" />
            </div>
            <h2 className="text-lg font-semibold">Branding</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Color Primario</label>
              <div className="flex items-center gap-3 mt-1">
                <div
                  className="w-10 h-10 rounded-lg border border-gray-200"
                  style={{ backgroundColor: empresa.branding?.color_primario || "#2563EB" }}
                />
                <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                  {empresa.branding?.color_primario || "#2563EB"}
                </code>
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">Logo URL</label>
              <p className="text-sm text-gray-500">{empresa.branding?.logo_url || "No configurado"}</p>
            </div>
          </div>
        </div>

        {/* Departments */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-green-50 rounded-lg">
              <Building2 size={20} className="text-green-600" />
            </div>
            <h2 className="text-lg font-semibold">Departamentos Activos</h2>
          </div>

          <div className="space-y-3">
            {Object.entries(departamentos).map(([key, dept]: [string, any]) => (
              <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium">{deptLabels[key] || key}</span>
                <span className={`badge ${dept.activo ? "badge-green" : "badge-gray"}`}>
                  {dept.activo ? "Activo" : "Inactivo"}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Integrations */}
        <div className="card lg:col-span-2">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-orange-50 rounded-lg">
              <Building2 size={20} className="text-orange-600" />
            </div>
            <h2 className="text-lg font-semibold">Integraciones</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Google Workspace</span>
                <span className={`badge ${integraciones.google_workspace?.activo ? "badge-green" : "badge-gray"}`}>
                  {integraciones.google_workspace?.activo ? "Conectado" : "No conectado"}
                </span>
              </div>
              <p className="text-xs text-gray-500">
                {integraciones.google_workspace?.carpeta_drive || "Sin configurar"}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Telegram</span>
                <span className={`badge ${integraciones.telegram?.activo ? "badge-green" : "badge-gray"}`}>
                  {integraciones.telegram?.activo ? "Activo" : "Inactivo"}
                </span>
              </div>
              <p className="text-xs text-gray-500">Bot de mensajería</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Calendario</span>
                <span className={`badge ${integraciones.calendario?.activo ? "badge-green" : "badge-gray"}`}>
                  {integraciones.calendario?.activo ? "Conectado" : "No conectado"}
                </span>
              </div>
              <p className="text-xs text-gray-500">
                {integraciones.calendario?.proveedor || "Sin proveedor"}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
