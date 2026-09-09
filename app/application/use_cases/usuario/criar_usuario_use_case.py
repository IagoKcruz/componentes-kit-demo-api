import bcrypt
from app.domain.entities.usuario import Usuario
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.validacao_error import ValidacaoError
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.mappers.usuario_mapper import UsuarioMapper


class CriarUsuarioUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, dto: CriarUsuarioDTO) -> UsuarioResponseDTO:
        async with self._uow as uow:
            if await uow.usuarios.buscar_por_email(dto.email):
                raise ValidacaoError("E-mail já cadastrado")

            if await uow.usuarios.buscar_por_cpf(dto.cpf):
                raise ValidacaoError("CPF já cadastrado")

            senha_hash = bcrypt.hashpw(dto.senha.encode(), bcrypt.gensalt()).decode()

            usuario = Usuario.criar(
                nome=dto.nome,
                email=dto.email,
                cpf=dto.cpf,
                senha_hash=senha_hash,
                tipos=dto.tipos,
            )

            salvo = await uow.usuarios.salvar(usuario)
            await uow.commit()
            return UsuarioMapper.para_response_dto(salvo)
