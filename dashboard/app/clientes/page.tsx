import { getClients, getClientStats } from "@/lib/data";
import { Users, Mail, Phone } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function ClientesPage() {
  const clients = await getClients();
  const stats = await getClientStats();

  const statusOrder = ["lead", "prospecto", "cotizado", "negociacion", "contratado", "en_produccion", "completado"];
  const statusLabels: Record<string, string> = {
    lead: "Lead",
    prospecto: "Prospecto",
    cotizado: "Cotizado",
    negociacion: "Negociación",
    contratado: "Contratado",
    en_produccion: "En producción",
    completado: "Completado",
    perdido: "Perdido",
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
        <p className="text-gray-500 mt-1">Gestión de clientes y prospectos</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {statusOrder.map((status) => {
          const count = stats.byStatus[status] || 0;
          if (count === 0) return null;
          return (
            <div key={status} className="card text-center">
              <p className="text-2xl font-bold text-primary-600">{count}</p>
              <p className="text-sm text-gray-500 capitalize">{statusLabels[status]}</p>
            </div>
          );
        })}
      </div>

      {/* Clients Table */}
      <div className="card overflow-x-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Lista de Clientes</h2>
          <span className="text-sm text-gray-500">{clients.length} total</span>
        </div>

        {clients.length === 0 ? (
          <div className="text-center py-12">
            <Users size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">No hay clientes registrados aún.</p>
            <p className="text-sm text-gray-400 mt-1">
              Habla con Hermes por Telegram: "Registra un cliente nuevo"
            </p>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">ID</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Nombre</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Contacto</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Estado</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Registro</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((client: any) => (
                <tr key={client.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm font-mono text-gray-500">{client.id}</td>
                  <td className="py-3 px-4">
                    <p className="font-medium text-sm">{client.nombre}</p>
                    {client.tipo_proyecto && (
                      <p className="text-xs text-gray-500">{client.tipo_proyecto}</p>
                    )}
                  </td>
                  <td className="py-3 px-4 text-sm">
                    {client.email && (
                      <div className="flex items-center gap-1 text-gray-600">
                        <Mail size={12} />
                        <span className="text-xs">{client.email}</span>
                      </div>
                    )}
                    {client.telefono && (
                      <div className="flex items-center gap-1 text-gray-600 mt-0.5">
                        <Phone size={12} />
                        <span className="text-xs">{client.telefono}</span>
                      </div>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`badge ${
                      client.estado === "contratado" ? "badge-green" :
                      client.estado === "cotizado" ? "badge-yellow" :
                      client.estado === "negociacion" ? "badge-blue" :
                      client.estado === "lead" ? "badge-gray" : "badge-purple"
                    }`}>
                      {statusLabels[client.estado] || client.estado}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-500">
                    {new Date(client.fecha_registro).toLocaleDateString("es-MX")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
